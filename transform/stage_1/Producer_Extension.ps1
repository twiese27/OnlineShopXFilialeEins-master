$Import_Path_F = 'transform/stage_1/transform_exports/fi/PRODUCER.csv'
$Import_Path_O = 'dumps/os/PRODUCER.csv'

$Export_Path_Extension_F = 'transform/stage_1/transform_exports/fi/PRODUCER_EXTENSION.csv'
$Export_Path_Extension_O = 'transform/stage_1/transform_exports/os/PRODUCER_EXTENSION.csv'
$Export_Path_POS_TO_Extension_F = 'transform/stage_1/transform_exports/fi/POS_TO_PRODUCER_EXTENSION.csv'
$Export_Path_POS_TO_Extension_O = 'transform/stage_1/transform_exports/os/POS_TO_PRODUCER_EXTENSION.csv'

$Data_F = Import-Csv -Path $Import_Path_F -Delimiter ";" -Encoding UTF8 | Select-Object PRODUCER_ID
$Data_O =Import-Csv -Path $Import_Path_O -Delimiter "," -Encoding UTF8 | Select-Object PRODUCER_ID

# PRODUCER_EXTENSION_F
$CSV_Header = 'PRODUCER_EXTENSION_ID;PRODUCER_ID'
$CSV_Header | Out-File $Export_Path_Extension_F -Encoding utf8

foreach ($Entry in $Data_F) {
    $CSV_New_Row = "$($Entry.PRODUCER_ID);$($Entry.PRODUCER_ID)"
    $CSV_New_Row | Out-File $Export_Path_Extension_F -Append -Encoding utf8    
}
# PRODUCER_EXTENSION_O
$CSV_Header = 'PRODUCER_EXTENSION_ID;PRODUCER_ID'
$CSV_Header | Out-File $Export_Path_Extension_O -Encoding utf8

foreach ($Entry in $Data_O) {
    $CSV_New_Row = "$($Entry.PRODUCER_ID);$($Entry.PRODUCER_ID)"
    $CSV_New_Row | Out-File $Export_Path_Extension_O -Append -Encoding utf8    
}

# POS_TO_PRODUCER_EXTENSION_F
$CSV_Header = 'PRODUCER_EXTENSION_ID;PRODUCER_ID;POINT_OF_SALE_ID'
$CSV_Header | Out-File $Export_Path_POS_TO_Extension_F -Encoding utf8

foreach ($Entry in $Data_F) {
    $CSV_New_Row = "$($Entry.PRODUCER_ID);$($Entry.PRODUCER_ID);1"
    $CSV_New_Row | Out-File $Export_Path_POS_TO_Extension_F -Append -Encoding utf8    
}

# POS_TO_PRODUCER_EXTENSION_O
$CSV_Header = 'PRODUCER_EXTENSION_ID;PRODUCER_ID;POINT_OF_SALE_ID'
$CSV_Header | Out-File $Export_Path_POS_TO_Extension_O -Encoding utf8

foreach ($Entry in $Data_O) {
    $CSV_New_Row = "$($Entry.PRODUCER_ID);$($Entry.PRODUCER_ID);2"
    $CSV_New_Row | Out-File $Export_Path_POS_TO_Extension_O -Append -Encoding utf8    
}
