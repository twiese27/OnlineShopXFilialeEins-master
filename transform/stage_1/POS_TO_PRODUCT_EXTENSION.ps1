$Import_Path_PRODUCT_EXTENSION_F = 'transform/stage_1/transform_exports/fi/PRODUCT_EXTENSION.csv'
$Import_Path_PLACE_OF_SALE_SELLS_PRODUCT_F = 'dumps/fi/PLACE_OF_SALE_SELLS_PRODUCT.csv'
$Import_Path_PRODUCT_EXTENSION_O = 'transform/stage_1/transform_exports/os/PRODUCT_EXTENSION.csv'
$Export_Path_POS_TO_PRODUCT_EXTENSION_F = 'transform/stage_1/transform_exports/fi/POS_TO_PRODUCT_EXTENSION.csv'
$Export_Path_POS_TO_PRODUCT_EXTENSION_O = 'transform/stage_1/transform_exports/os/POS_TO_PRODUCT_EXTENSION.csv'

if (Test-Path -Path $Import_Path_PRODUCT_EXTENSION_F) { 
    if (Test-Path -Path $Import_Path_PLACE_OF_SALE_SELLS_PRODUCT_F) { 
        if (Test-Path -Path $Import_Path_PLACE_OF_SALE_SELLS_PRODUCT_F) {
            $Data_F = Import-CSV -Path $Import_Path_PRODUCT_EXTENSION_F -Delimiter ";" -Encoding UTF8 | Select-Object PRODUCT_EXTENSION_ID, PRODUCT_ID, SHELF_HEIGHT, SHELF_DEPTH
            $Date_2_F = Import-CSV -Path $Import_Path_PLACE_OF_SALE_SELLS_PRODUCT_F -Delimiter ";" -Encoding UTF8 | Select-Object PLACE_OF_SALE_ID, PRODUCT_ID, MIN_AGE_REQUIREMENT, IS_BEING_SOLD
            $CSV_Header = 'POINT_OF_SALE_ID;PRODUCT_EXTENSION_ID;PRODUCT_ID;IS_BEING_SOLD;MIN_AGE_REQUIREMENT'
            $CSV_Header | Out-File $Export_Path_POS_TO_PRODUCT_EXTENSION_F -Encoding utf8

            foreach ($Entry in $Data_F) {
                $temp = $Date_2_F | Where-Object { $_.PRODUCT_ID -eq $($Entry.PRODUCT_ID) }
                $CSV_New_Row = "1;$($Entry.PRODUCT_EXTENSION_ID);$($Entry.PRODUCT_ID);$($temp.IS_BEING_SOLD);$($temp.MIN_AGE_REQUIREMENT)"
                $CSV_New_Row | Out-File $Export_Path_POS_TO_PRODUCT_EXTENSION_F -Append -Encoding utf8    
            }
            $Data_O = Import-CSV -Path $Import_Path_PRODUCT_EXTENSION_O -Delimiter ";" -Encoding UTF8 | Select-Object PRODUCT_EXTENSION_ID, PRODUCT_ID, SHELF_HEIGHT, SHELF_DEPTH
            $CSV_Header = 'POINT_OF_SALE_ID;PRODUCT_EXTENSION_ID;PRODUCT_ID;IS_BEING_SOLD;MIN_AGE_REQUIREMENT'
            $CSV_Header | Out-File $Export_Path_POS_TO_PRODUCT_EXTENSION_O -Encoding utf8

            foreach ($Entry in $Data_O) {
                $CSV_New_Row = "2;$($Entry.PRODUCT_EXTENSION_ID);$($Entry.PRODUCT_ID);1;"
                $CSV_New_Row | Out-File $Export_Path_POS_TO_PRODUCT_EXTENSION_O -Append -Encoding utf8    
            }
        } else {
            Write-Host "Import data Point_of_Sale_sells_Product not found"
        }
    }else {
        Write-Host "Import data Onlineshop not found"
    }
}else {
    Write-Host "Import data Filiale not found"
}