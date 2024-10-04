# Dieses Script ist kein Transform Script. Es gleicht ausschließlich die Producer aus den Produkten,
# mit der händisch erstellten csv ab, ob sicher zugehen, dass alle Producer übernommen werden

$Import_Path_1 = 'transform/stage_1/transform_exports/fi/PRODUCER.csv'
$Import_Path_2 = 'dumps/fi/PRODUCT.csv'

$Data_1 = Import-Csv -Path $Import_Path_1 -Delimiter ";" -Encoding UTF8 | Select-Object Name
$Data_2 = Import-Csv -Path $Import_Path_2 -Delimiter ";" -Encoding UTF8 | Select-Object Brand

$Array = @()
foreach ($name in $Data_2.Brand) {
    if ($Array -notcontains $name) {
        $Array += $name
    }
}
$Data_1 = $Data_1 | Sort-Object
$Array = $Array | Sort-Object

# Vergleich der beiden Arrays: 
# - Gemeinsame Einträge
$CommonEntries = $Data_1.Name | Where-Object { $Array -contains $_ }

# - Nur in Data_1
$OnlyInArray1 = $Data_1.Name | Where-Object { $Array -notcontains $_ }

# - Nur in Array
$OnlyInArray2 = $Array | Where-Object { $Data_1.Name -notcontains $_ }

# Ergebnis als Objekt erstellen, um CSV zu exportieren
$ComparisonResult = @()

foreach ($name in $CommonEntries) {
    $ComparisonResult += [pscustomobject]@{
        "Name" = $name
        "Status" = "Gleich"
    }
}

foreach ($name in $OnlyInArray1) {
    $ComparisonResult += [pscustomobject]@{
        "Name" = $name
        "Status" = "Nur in der vorbereiteten CSV"
    }
}

foreach ($name in $OnlyInArray2) {
    $ComparisonResult += [pscustomobject]@{
        "Name" = $name
        "Status" = "Nur in den Produkten"
    }
}

# Export als CSV
$ComparisonResult | Export-Csv -Path 'transform/stage_1/ABGLEICH_PRODUCER_FILIALE.csv' -NoTypeInformation -Encoding UTF8

Write-Host "Der Vergleich wurde abgeschlossen und als CSV exportiert."
