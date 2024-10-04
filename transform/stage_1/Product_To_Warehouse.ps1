$Import_Path = 'transform/stage_1/STOCK_Filiale.csv'

$Export_Path = 'transform/stage_1/transform_exports/fi/PRODUCT_TO_WAREHOUSE.csv'

$Data = Import-Csv -Path $Import_Path -Delimiter ";" -Encoding UTF8 | Select-Object PRODUCT_ID, STOCK

function Generate-RandomString {
    # Generiere eine Zufallszahl zwischen 1 und 9 und formatiere sie auf 3 Stellen mit führenden Nullen
    $firstPart = "{0:D3}" -f (Get-Random -Minimum 1 -Maximum 10)
    
    # Wähle zwei zufällige Großbuchstaben
    $secondPart = [char](Get-Random -Minimum 65 -Maximum 91)
    $thirdPart = [char](Get-Random -Minimum 65 -Maximum 91)
    
    # Generiere eine Zufallszahl zwischen 1 und 99 und formatiere sie auf 2 Stellen mit führenden Nullen
    $fourthPart = "{0:D2}" -f (Get-Random -Minimum 1 -Maximum 100)
    
    # Verbinde alle Teile zu einem String
    return "$firstPart$secondPart$thirdPart$fourthPart"
}

$CSV_Header = 'PRODUCT_ID;WAREHOUSE_ID;STOCK;STORAGE_LOCATION'
$CSV_Header | Out-File $Export_Path -Encoding utf8

foreach ($Entry in $Data) {
    $STORAGE_LOCATION = Generate-RandomString
    $CSV_New_Row = "$($Entry.PRODUCT_ID);1;$($Entry.STOCK);$STORAGE_LOCATION"
    $CSV_New_Row | Out-File $Export_Path_F -Append -Encoding utf8 
}