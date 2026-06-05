from source.application.file_handler import TargetFileHandler, SourceFileHandler
from source.model.dto import ReadingInfo, StatusEnum, ColumnToRead, search


def merge_all(column_values: list[str],
              id_column: str,
              source_file_path: str,
              target_files: list[str],
              logger,
              progress_callback,
              infobox_callback,
              end_handle_callback):
    center = len(column_values) // 2
    columns = []
    for i in range(center + 1):
        columns.append(ColumnToRead(column_values[i], column_values[i + center]))
    reading_info = ReadingInfo(
        id_column_name=id_column,
        columns_for_copy=columns,
    )
    logger.info(f"Parsed reading info: {reading_info}")
    infobox_callback(f"Открывается файл: {source_file_path}\n")
    source_handler = SourceFileHandler(reading_info, source_file_path)
    id_to_source_item = {source_item.id: source_item for source_item in source_handler.read_file()}
    infobox_callback(f"Открыт файл: {source_file_path}\n")
    logger.info(f"Read {len(id_to_source_item.values())} source items")
    logger.info(f"IDs: {len(id_to_source_item.keys())}")
    files_count = 0

    target_file_path = ""
    for file in target_files:
        try:
            logger.info(f"Processing file: {file}")
            target_file_path = file
            file_handler = TargetFileHandler(target_file_path)
            infobox_callback(f"Открывается файл: {target_file_path}\n")
            df = file_handler.read_file()
            infobox_callback(f"Обрабатывается файл: {target_file_path}\n")
            logger.info(f"Read file: {file}")

            handled_rows_count = 0
            row_count = len(df)
            for idx, row in df.iterrows():
                id_value = row[reading_info.id_column_name]
                if id_value in id_to_source_item:
                    for source_column in id_to_source_item[id_value].columns:
                        source_status = source_column.status
                        source_value = source_column.value
                        target_status = search(row[source_column.status_name])
                        target_value = row[source_column.name]
                        if source_status.need_to_refresh(target_status) and source_value != target_value:
                            logger.info(
                                f'idx: {id_value}, {source_column.name}, source: {source_status, source_value}, target: {target_status, target_value}')
                            df.loc[idx, source_column.name] = source_value
                            df.loc[idx, source_column.status_name] = source_status.str_value
                handled_rows_count += 1
                row_percentage = handled_rows_count / row_count
                row_percentage_in_one_file_percent = round(row_percentage * 100 / len(target_files))
                percentage = round(100 * (files_count / len(target_files))) + row_percentage_in_one_file_percent
                progress_callback(percentage)
                print(
                    f"From {row_count} handled {handled_rows_count} rows, percentage: {percentage}%"
                )

            infobox_callback(f"Cохраняется файл: {target_file_path}\n")
            file_handler.save_df()
            infobox_callback(f"Обработан файл: {target_file_path}\n")
            logger.info(f"Finished processing file: {file}")
            files_count += 1
        except Exception as ex:
            infobox_callback(f"В процессе обработки файла {target_file_path} произошла ошибка\n")
            logger.info(f"Finished processing file: {file} with exception: {ex}")
            files_count += 1
        percentage = round(100 * (files_count / len(target_files)))
        progress_callback(percentage)

        logger.info(f"From {len(target_files)} files handled {files_count} files, percentage: {percentage}%")
    end_handle_callback()
