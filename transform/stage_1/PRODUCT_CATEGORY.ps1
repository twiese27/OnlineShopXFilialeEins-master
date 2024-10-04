# 
$Import_Path_F = 'transform/stage_1/transform_exports/fi/PRODUCT_CATEGORY.csv'
$Import_Path_O = 'dumps/os/PRODUCT_CATEGORY.csv'

$Export_Path_Extension_F = 'transform/stage_1/transform_exports/fi/PRODUCT_CATEGORY_EXTENSION.csv'
$Export_Path_Extension_O = 'transform/stage_1/transform_exports/os/PRODUCT_CATEGORY_EXTENSION.csv'
$Export_Path_POS_TO_Extension_F = 'transform/stage_1/transform_exports/fi/POS_TO_PRODUCT_CATEGORY_EXTENSION.csv'
$Export_Path_POS_TO_Extension_O = 'transform/stage_1/transform_exports/os/POS_TO_PRODUCT_CATEGORY_EXTENSION.csv'

$Nur_In_O = @('169','170','171','172','173','174')

$Data_F = Import-Csv -Path $Import_Path_F -Delimiter ";" -Encoding UTF8 | Select-Object PRODUCT_CATEGORY_ID, NAME, PARENT_CATEGORY
$Data_O = Import-Csv -Path $Import_Path_O -Delimiter ";" -Encoding UTF8 | Select-Object PRODUCT_CATEGORY_ID, NAME, PARENT_CATEGORY

$CSV_Header = 'PRODUCT_CATEGORY_EXTENSION_ID;PRODUCT_CATEGORY_ID'
$CSV_Header | Out-File $Export_Path_Extension_O -Encoding utf8

foreach ($Entry in $Data_O) {
    $CSV_New_Row = "$($Entry.PRODUCT_CATEGORY_ID);$($Entry.PRODUCT_CATEGORY_ID)"
    $CSV_New_Row | Out-File $Export_Path_Extension_O -Append -Encoding utf8 
}

$CSV_Header = 'PRODUCT_CATEGORY_EXTENSION_ID;PRODUCT_CATEGORY_ID'
$CSV_Header | Out-File $Export_Path_Extension_F -Encoding utf8

foreach ($Entry in $Data_F) {
    $CSV_New_Row = "$($Entry.PRODUCT_CATEGORY_ID);$($Entry.PRODUCT_CATEGORY_ID)"
    $CSV_New_Row | Out-File $Export_Path_Extension_F -Append -Encoding utf8 
}

$CSV_Header = 'PRODUCT_CATEGORY_EXTENSION_ID;PRODUCT_CATEGORY_ID;POINT_OF_SALE_ID'
$CSV_Header | Out-File $Export_Path_POS_TO_Extension_O -Encoding utf8

$CSV_Header = 'PRODUCT_CATEGORY_EXTENSION_ID;PRODUCT_CATEGORY_ID;POINT_OF_SALE_ID'
$CSV_Header | Out-File $Export_Path_POS_TO_Extension_F -Encoding utf8

foreach ($Entry in $Data_O) {
    if ($Entry.PRODUCT_CATEGORY_ID -notin $Nur_In_O) {
        $CSV_New_Row = "$($Entry.PRODUCT_CATEGORY_ID);$($Entry.PRODUCT_CATEGORY_ID);2"
        $CSV_New_Row | Out-File $Export_Path_POS_TO_Extension_O -Append -Encoding utf8 

        $CSV_New_Row = "$($Entry.PRODUCT_CATEGORY_ID);$($Entry.PRODUCT_CATEGORY_ID);1"
        $CSV_New_Row | Out-File $Export_Path_POS_TO_Extension_F -Append -Encoding utf8 
    } else {
        $CSV_New_Row = "$($Entry.PRODUCT_CATEGORY_ID);$($Entry.PRODUCT_CATEGORY_ID);2"
        $CSV_New_Row | Out-File $Export_Path_POS_TO_Extension_O -Append -Encoding utf8 
    }
}

foreach ($Entry in $Data_F) {
    $CSV_New_Row = "$($Entry.PRODUCT_CATEGORY_ID);$($Entry.PRODUCT_CATEGORY_ID);1"
    $CSV_New_Row | Out-File $Export_Path_POS_TO_Extension_F -Append -Encoding utf8 
}