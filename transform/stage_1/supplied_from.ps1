#Supplied_From Filiale - OS hat den gesammten Strang nicht
$Import_Path = 'dumps/fi/batch_supplier_order_join.csv'
$Export_Path_Product_Supplied_From_Supplier_F = 'transform/stage_1/transform_exports/fi/PRODUCT_TO_SUPPLIER.csv'
$Export_Path_Supplied_From_Extension_F = 'transform/stage_1/transform_exports/fi/SUPPLIED_FROM_EXTENSION.csv'
$Export_Path_Product_Supplier_Supplied_From_Extension_F = 'transform/stage_1/transform_exports/fi/PRODUCT_TO_SUPPLIER_TO_SUPPLIED_FROM_EXTENSION.csv'

if (Test-Path -Path $Import_Path) { 
    $Data = Import-CSV -Path $Import_Path -Delimiter ";" -Encoding UTF8 | Select-Object BATCH_ID, PRODUCT_ID, ORDER_ID, NUMBER_OF_CASES, WEIGHT, MANUFACTORING_DATE, BBD, SUPPLIER_ORDER_ID, SUPPLIER_ID, ORDER_DATE, DELIVERY_DATE, PRICE
    #Product_to_Supplier
    $CSV_Header = 'PRODUCT_ID;SUPPLIER_ID;PURCHASE_PRICE'
    $CSV_Header | Out-File $Export_Path_Product_Supplied_From_Supplier_F -Encoding utf8

    $ExistingData = Import-CSV -Path $Export_Path_Product_Supplied_From_Supplier_F -Delimiter ";" -Encoding UTF8 | Select-Object PRODUCT_ID, SUPPLIER_ID
    $Lookup = @{}
    foreach ($row in $ExistingData) {
        $key = "$($row.PRODUCT_ID)|$($row.SUPPLIER_ID)"
        $Lookup[$key] = $true
    }

    foreach ($Entry in $Data) {
        $key = "$($Entry.PRODUCT_ID)|$($Entry.SUPPLIER_ID)"

        if (-not $Lookup.ContainsKey($key)) {
            $CSV_New_Row = "$($Entry.PRODUCT_ID);$($Entry.SUPPLIER_ID);"
            $CSV_New_Row | Out-File $Export_Path_Product_Supplied_From_Supplier_F -Append -Encoding utf8

            $Lookup[$key] = $true
        }
    }
    # Die spezielle Kombination, die geprüft oder hinzugefügt werden soll
    $Special_Product_ID = 8
    $Special_Supplier_ID = 5
    $Special_Price = "" # Du kannst den Preis hier anpassen, falls gewünscht

    # Spezielle Kombination prüfen: PRODUCT_ID = 8 und SUPPLIER_ID = 5
    $specialKey = "$Special_Product_ID|$Special_Supplier_ID"
    if (-not $Lookup.ContainsKey($specialKey)) {
        # Falls die Kombination nicht existiert, hinzufügen
        $CSV_New_Row = "$Special_Product_ID;$Special_Supplier_ID;$Special_Price"
        $CSV_New_Row | Out-File $Export_Path_Product_Supplied_From_Supplier_F -Append -Encoding utf8
        Write-Host "Spezielle Zeile wurde hinzugefügt: PRODUCT_ID = $Special_Product_ID, SUPPLIER_ID = $Special_Supplier_ID"
    } else {
        Write-Host "Die spezielle Kombination PRODUCT_ID = $Special_Product_ID und SUPPLIER_ID = $Special_Supplier_ID existiert bereits."
    }

    #Supplied_From_Extension and Product_Supplier_Supplied_From_Extension
    $CSV_Header = 'BATCH_ID;NUMBER_OF_CASES;WEIGHT;MANUFACTORING_DATE;BBD;ORDER_DATE;DELIVERY_DATE;SUPPLIER_ORDER_PRICE;SUPPLIER_ORDER_ID;POINT_OF_SALE_ID'
    $CSV_Header | Out-File $Export_Path_Supplied_From_Extension_F -Encoding utf8

    $CSV_Header = 'PRODUCT_ID;SUPPLIER_ID;BATCH_ID;PURCHASE_PRICE'
    $CSV_Header | Out-File $Export_Path_Product_Supplier_Supplied_From_Extension_F -Encoding utf8

    foreach ($Entry in $Data) {
        if ($Entry.SUPPLIER_ORDER_ID -like "240") {
            $CSV_New_Row = "$($Data.length);5;1210.96;2024-06-01 00:00:00;2024-12-05 00:00:00;2024-01-07 00:00:00;2024-01-09 00:00:00;6502.69;240;1"
            $CSV_New_Row | Out-File $Export_Path_Supplied_From_Extension_F -Append -Encoding utf8
            $temp = $Data.length + 1
            $CSV_New_Row = "$temp;5;1210.96;2024-06-01 00:00:00;2024-12-05 00:00:00;2024-01-07 00:00:00;2024-01-09 00:00:00;6502.69;240;1"
            $CSV_New_Row | Out-File $Export_Path_Supplied_From_Extension_F -Append -Encoding utf8
        
            $CSV_New_Row = "8;5;$($Data.length);"
            $CSV_New_Row | Out-File $Export_Path_Product_Supplier_Supplied_From_Extension_F -Append -Encoding utf8    
            
            $CSV_New_Row = "8;5;$temp;"
            $CSV_New_Row | Out-File $Export_Path_Product_Supplier_Supplied_From_Extension_F -Append -Encoding utf8    
        } else {
            $CSV_New_Row = "$($Entry.BATCH_ID);$($Entry.NUMBER_OF_CASES);$($Entry.WEIGHT);$($Entry.MANUFACTORING_DATE);$($Entry.BBD);$($Entry.ORDER_DATE);$($Entry.DELIVERY_DATE);$($Entry.PRICE);$($Entry.SUPPLIER_ORDER_ID);1"
            $CSV_New_Row | Out-File $Export_Path_Supplied_From_Extension_F -Append -Encoding utf8
    
            $CSV_New_Row = "$($Entry.PRODUCT_ID);$($Entry.SUPPLIER_ID);$($Entry.BATCH_ID);"
            $CSV_New_Row | Out-File $Export_Path_Product_Supplier_Supplied_From_Extension_F -Append -Encoding utf8    
        }
    }
} else {
    Write-Host "Import data Filiale not found"
}

