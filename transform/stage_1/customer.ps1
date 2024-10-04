#Customer
$Import_Path_F = 'dumps/fi/customer_customer_has_address_address_join.csv'
$Import_Path_O = 'dumps/os/CUSTOMER.csv'
$Export_Path_Customer_F = 'transform\stage_1\transform_exports\fi\CUSTOMER.csv'
$Export_Path_Customer_Extension_F = 'transform/stage_1/transform_exports/fi/CUSTOMER_EXTENSION.csv'
$Export_Path_Customer_Extension_O = 'transform/stage_1/transform_exports/os/CUSTOMER_EXTENSION.csv'
$Export_Path_Customer_Billing_Address_F = 'transform/stage_1/transform_exports/fi/CUSTOMER_BILLING_ADDRESS.csv'
$Export_Path_POS_To_Customer_Extension_F = 'transform/stage_1/transform_exports/fi/POS_TO_CUSTOMER_EXTENSION.csv'
$Export_Path_POS_To_Customer_Extension_O = 'transform/stage_1/transform_exports/os/POS_TO_CUSTOMER_EXTENSION.csv'
$Export_Path_POS_TO_Customer_Billing_Address_F = 'transform/stage_1/transform_exports/fi/POS_TO_CUSTOMER_BILLING_ADDRESS.csv'

$Customer_without_PostCode = @('1','2','3','4','5')
$Customer_without_PostCode_PostCodes = @('26121','26123','26125','26127','26129')

if (Test-Path -Path $Import_Path_F) {
    if (Test-Path -Path $Import_Path_O) {
        $Data_F = Import-CSV -Path $Import_Path_F -Delimiter ";" -Encoding UTF8 | Select-Object CUSTOMER_ID, CUSTOMER_FIRST_NAME, CUSTOMER_LAST_NAME, CUSTOMER_EMAIL, CUSTOMER_GENDER, CUSTOMER_BIRTH_DATE, ADDRESS_ID, COUNTRY, CITY, POSTCODE, STREET, HOUSE_NUMBER, ADDITIONAL_ADDRESS_INFORMATION, TYPE
        $Data_O = Import-CSV -Path $Import_Path_O -Delimiter ";" -Encoding UTF8 | Select-Object CUSTOMER_ID, STREET, HOUSE_NUMBER, POSTAL_CODE, CITY, MIDDLE_NAME, LASTNAME, IBAN, BIRTH_DATE, CREATED_ON, EMAIL, COUNTRY, FORENAME
        #Customer_F
        $CSV_Header = 'CUSTOMER_ID;STREET;HOUSE_NUMBER;POSTAL_CODE;CITY;MIDDLE_NAME;LASTNAME;IBAN;BIRTH_DATE;CREATED_ON;EMAIL;COUNTRY;FORENAME'
        $CSV_Header | Out-File $Export_Path_Customer_F -Encoding utf8

        foreach ($Entry in $Data_F) {
            if ($Entry.TYPE -like "delivery") {
                if ($Entry.CUSTOMER_ID -notin $Customer_without_PostCode) {
                    if ($Entry.COUNTRY -like "Deutschland") {
                        $CSV_New_Row = "$($Entry.CUSTOMER_ID);$($Entry.STREET);$($Entry.HOUSE_NUMBER);$($Entry.POSTCODE);$($Entry.CITY);;$($Entry.CUSTOMER_LAST_NAME);;$($Entry.CUSTOMER_BIRTH_DATE);;$($Entry.CUSTOMER_EMAIL);Germany;$($Entry.CUSTOMER_FIRST_NAME)"
                        $CSV_New_Row | Out-File $Export_Path_Customer_F -Append -Encoding utf8
                    }else {
                        $CSV_New_Row = "$($Entry.CUSTOMER_ID);$($Entry.STREET);$($Entry.HOUSE_NUMBER);$($Entry.POSTCODE);$($Entry.CITY);;$($Entry.CUSTOMER_LAST_NAME);;$($Entry.CUSTOMER_BIRTH_DATE);;$($Entry.CUSTOMER_EMAIL);$($Entry.COUNTRY);$($Entry.CUSTOMER_FIRST_NAME)"
                        $CSV_New_Row | Out-File $Export_Path_Customer_F -Append -Encoding utf8
                    }
                } else {
                    $Customer_ID_as_Number = [int]$Entry.CUSTOMER_ID
                    $PostCode = $Customer_without_PostCode_PostCodes[($Customer_ID_as_Number - 1)]
                    Write-Host "PostCode muss ersetzt werden zu $PostCode"
                    if ($Entry.COUNTRY -like "Deutschland") {
                        $CSV_New_Row = "$($Entry.CUSTOMER_ID);$($Entry.STREET);$($Entry.HOUSE_NUMBER);$PostCode;$($Entry.CITY);;$($Entry.CUSTOMER_LAST_NAME);;$($Entry.CUSTOMER_BIRTH_DATE);;$($Entry.CUSTOMER_EMAIL);Germany;$($Entry.CUSTOMER_FIRST_NAME)"
                        $CSV_New_Row | Out-File $Export_Path_Customer_F -Append -Encoding utf8
                    }else {
                        $CSV_New_Row = "$($Entry.CUSTOMER_ID);$($Entry.STREET);$($Entry.HOUSE_NUMBER);$PostCode;$($Entry.CITY);;$($Entry.CUSTOMER_LAST_NAME);;$($Entry.CUSTOMER_BIRTH_DATE);;$($Entry.CUSTOMER_EMAIL);$($Entry.COUNTRY);$($Entry.CUSTOMER_FIRST_NAME)"
                        $CSV_New_Row | Out-File $Export_Path_Customer_F -Append -Encoding utf8
                    }
                }
            }
        }
        #Customer_Billing_Address_F
        $CSV_Header = 'CUSTOMER_BILLING_ADDRESS_ID;STREET;CITY;HOUSE_NUMBER;COUNTRY;POSTAL_CODE;ADDITIONAL_ADDRESS_INFORMATION;CUSTOMER_ID'
        $CSV_Header | Out-File $Export_Path_Customer_Billing_Address_F -Encoding utf8

        $ID_Counter = 1
        foreach ($Entry in $Data_F) {
            if ($Entry.TYPE -like "billing") {
                if ($Entry.COUNTRY -like "Deutschland") {
                    $CSV_New_Row = "$ID_Counter;$($Entry.STREET);$($Entry.CITY);$($Entry.HOUSE_NUMBER);Germany;$($Entry.POSTCODE);$($Entry.ADDITIONAL_ADDRESS_INFORMATION);$($Entry.CUSTOMER_ID)"
                    $CSV_New_Row | Out-File $Export_Path_Customer_Billing_Address_F -Append -Encoding utf8
                }else {
                    $CSV_New_Row = "$ID_Counter;$($Entry.STREET);$($Entry.CITY);$($Entry.HOUSE_NUMBER);$($Entry.COUNTRY);$($Entry.POSTCODE);$($Entry.ADDITIONAL_ADDRESS_INFORMATION);$($Entry.CUSTOMER_ID)"
                    $CSV_New_Row | Out-File $Export_Path_Customer_Billing_Address_F -Append -Encoding utf8
                }
                $ID_counter++
            }
        }

        #Customer_Extension_F
        $CSV_Header = 'CUSTOMER_EXTENSION_ID;CUSTOMER_ID;GENDER;ADDITIONAL_ADDRESS_INFORMATION'
        $CSV_Header | Out-File $Export_Path_Customer_Extension_F -Encoding utf8

        foreach ($Entry in $Data_F) {
            if ($Entry.TYPE -like "delivery") {
                $CSV_New_Row = "$($Entry.CUSTOMER_ID);$($Entry.CUSTOMER_ID);$($Entry.CUSTOMER_GENDER);$($Entry.ADDITIONAL_ADDRESS_INFORMATION)"
                $CSV_New_Row | Out-File $Export_Path_Customer_Extension_F -Append -Encoding utf8
            }
        }

        #Customer_Extension_O
        $CSV_Header = 'CUSTOMER_EXTENSION_ID;CUSTOMER_ID;GENDER;ADDITIONAL_ADDRESS_INFORMATION'
        $CSV_Header | Out-File $Export_Path_Customer_Extension_O -Encoding utf8

        foreach ($Entry in $Data_O) {
                $CSV_New_Row = "$($Entry.CUSTOMER_ID);$($Entry.CUSTOMER_ID);;"
                $CSV_New_Row | Out-File $Export_Path_Customer_Extension_O -Append -Encoding utf8
        }

        #POS_To_Customer_Extension_F
        $Data_Customer_Extension_F = Import-CSV -Path $Export_Path_Customer_Extension_F -Delimiter ";" -Encoding UTF8 | Select-Object CUSTOMER_EXTENSION_ID, CUSTOMER_ID, GENDER, ADDITIONAL_ADDRESS_INFORMATION

        $CSV_Header = 'CUSTOMER_EXTENSION_ID;CUSTOMER_ID;POINT_OF_SALE_ID'
        $CSV_Header | Out-File $Export_Path_POS_To_Customer_Extension_F -Encoding utf8

        foreach ($Entry in $Data_Customer_Extension_F) {
            $CSV_New_Row = "$($Entry.CUSTOMER_EXTENSION_ID);$($Entry.CUSTOMER_ID);1"
            $CSV_New_Row | Out-File $Export_Path_POS_To_Customer_Extension_F -Append -Encoding utf8
        }

        #POS_To_Customer_Extension_O
        $Data_Customer_Extension_O = Import-CSV -Path $Export_Path_Customer_Extension_O -Delimiter ";" -Encoding UTF8 | Select-Object CUSTOMER_EXTENSION_ID, CUSTOMER_ID, GENDER, ADDITIONAL_ADDRESS_INFORMATION

        $CSV_Header = 'CUSTOMER_EXTENSION_ID;CUSTOMER_ID;POINT_OF_SALE_ID'
        $CSV_Header | Out-File $Export_Path_POS_To_Customer_Extension_O -Encoding utf8

        foreach ($Entry in $Data_Customer_Extension_O) {
            $CSV_New_Row = "$($Entry.CUSTOMER_EXTENSION_ID);$($Entry.CUSTOMER_ID);2"
            $CSV_New_Row | Out-File $Export_Path_POS_To_Customer_Extension_O -Append -Encoding utf8
        }

        #POS_To_Customer_Billing_Address_F
        $Data_Customer_Billing_Address_F = Import-CSV -Path $Export_Path_Customer_Billing_Address_F -Delimiter ";" -Encoding UTF8 | Select-Object CUSTOMER_BILLING_ADDRESS_ID, STREET, CITY, HOUSE_NUMBER, COUNTRY, POSTAL_CODE, ADDITIONAL_ADDRESS_INFORMATION, CUSTOMER_ID

        $CSV_Header = 'POINT_OF_SALE_ID;CUSTOMER_BILLING_ADDRESS_ID'
        $CSV_Header | Out-File $Export_Path_POS_To_Customer_Billing_Address_F -Encoding utf8

        foreach ($Entry in $Data_Customer_Billing_Address_F) {
            $CSV_New_Row = "1;$($Entry.CUSTOMER_BILLING_ADDRESS_ID)"
            $CSV_New_Row | Out-File $Export_Path_POS_To_Customer_Billing_Address_F -Append -Encoding utf8
        }

    } else {
        Write-Host "Import data Onlineshop not found"
    }
} else {
    Write-Host "Import data Filiale not found"
}