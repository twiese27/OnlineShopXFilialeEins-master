import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class Employee {

    public static void main(String[] args) {
        String employeeFilialeSourceCsv = "dumps/fi/employee_to_address_join.csv"; // Quell CSV-Datei für EMPLOYEE_FILIALE und EMPLOYEE_EXTENSION_FILIALE
        String employeeOnlineshopSourceCsv = "dumps/os/EMPLOYEE.csv"; // CSV-Datei für EMPLOYEE_EXTENSION_ONLINESHOP
        String employeeFilialeCsv = "transform/stage_1/transform_exports/fi/EMPLOYEE.csv"; // Ziel CSV-Datei für EMPLOYEE_FILIALE
        String employeeExtensionFilialeCsv = "transform/stage_1/transform_exports/fi/EMPLOYEE_EXTENSION.csv"; // Ziel CSV-Datei für EMPLOYEE_EXTENSION_FILIALE
        String employeeExtensionOnlineshopCsv = "transform/stage_1/transform_exports/os/EMPLOYEE_EXTENSION.csv"; // Ziel CSV-Datei für EMPLOYEE_EXTENSION_ONLINESHOP
        Integer[] roleHelper = new Integer[]{16, 13, 14, 22, 22, 22, 22, 22, 21, 21, 21, 18, 15, 22, 22, 21, 17, 22, 22, 21, 7, 22, 22, 21, 19, 22, 22, 21, 2, 20};

        // Zähler für EMPLOYEE_EXTENSION_ID
        int employeeIdCounter = 1;

        try (BufferedReader br = new BufferedReader(new FileReader(employeeFilialeSourceCsv));
             BufferedWriter employeeFilialeWriter = new BufferedWriter(new FileWriter(employeeFilialeCsv));
             BufferedWriter employeeExtensionWriter = new BufferedWriter(new FileWriter(employeeExtensionFilialeCsv));
             BufferedReader employeeOnlineshopBr = new BufferedReader(new FileReader(employeeOnlineshopSourceCsv));
             BufferedWriter employeeOnlineshopWriter = new BufferedWriter(new FileWriter(employeeExtensionOnlineshopCsv))) {

            // Kopfzeilen für die Ziel-CSV-Dateien schreiben
            employeeFilialeWriter.write("EMPLOYEE_ID;HOUSE_NUMBER;CITY;POSTAL_CODE;COUNTRY;STREET;LASTNAME;FORENAME;MIDDLE_NAME;BIRTH_DATE;SALARY;IBAN;TAX_CLASS;WORKING_SINCE;WAREHOUSE_ID;ROLE_ID\n");
            employeeExtensionWriter.write("EMPLOYEE_EXTENSION_ID;EMPLOYEE_ID;BANK_NAME;BIC;WORKING_HOURS_PER_WEEK;PROVISION_RATE;ADDITIONAL_ADDRESS_INFORMATION;ADDRESS_TYPE;GENDER;EMAIL;PHONE_NUMBER\n");
            employeeOnlineshopWriter.write("EMPLOYEE_EXTENSION_ID;EMPLOYEE_ID;BANK_NAME;BIC;WORKING_HOURS_PER_WEEK;PROVISION_RATE;ADDITIONAL_ADDRESS_INFORMATION;ADDRESS_TYPE;GENDER;EMAIL;PHONE_NUMBER\n");

            String line;
            boolean firstLine = true;
            Random random = new Random();

            // Verarbeiten der source_employee.csv Datei für EMPLOYEE_FILIALE und EMPLOYEE_EXTENSION_FILIALE
            while ((line = br.readLine()) != null) {
                if (firstLine) {
                    // Kopfzeile der Quell CSV-Datei überspringen
                    firstLine = false;
                    continue;
                }

                // Spaltenwerte der Quell CSV-Datei aufteilen
                String[] values = line.split(";", -1);

                // EMPLOYEE_FILIALE CSV füllen
                String employeeId = values[0];
                String houseNumber = values[26];
                String city = values[23];
                String postalCode = values[24];
                String country = values[22].equals("Deutschland") ? "Germany" : values[22];
                String street = values[25];
                String lastName = values[4];
                String firstName = values[3];
                String middleName = ""; // Immer leer
                String birthDate = values[7].split(" ")[0]; // Nur Datum ohne Uhrzeit
                String salary = values[9];
                String iban = values[16];
                int taxClass = random.nextInt(5) + 1; // Random zwischen 1 und 5
                String workingSince = values[13].split(" ")[0]; // Nur Datum ohne Uhrzeit
                String warehouseId = ""; // Leer
                String roleId = roleHelper[employeeIdCounter - 1].toString(); // Immer "1"

                // Zeile in EMPLOYEE_FILIALE CSV schreiben
                employeeFilialeWriter.write(employeeId + ";" + houseNumber + ";" + city + ";" + postalCode + ";" + country + ";"
                        + street + ";" + lastName + ";" + firstName + ";" + middleName + ";" + birthDate + ";" + salary + ";" + iban + ";"
                        + taxClass + ";" + workingSince + ";" + warehouseId + ";" + roleId + "\n");

                // EMPLOYEE_EXTENSION_FILIALE CSV füllen
                String bankName = values[14];
                String bic = values[15];
                String workingHoursPerWeek = values[11];
                String provisionRate = values[10].replace(".", ","); // Tauschen von Punkt zu Komma für Provision
                String additionalAddressInfo = values[27];
                String addressType = values[28];
                String gender = values[6];
                String email = values[5];
                String phoneNumber = values[8];

                // Zeile in EMPLOYEE_EXTENSION_FILIALE CSV schreiben
                employeeExtensionWriter.write(employeeIdCounter + ";" + employeeId + ";" + bankName + ";" + bic + ";"
                        + workingHoursPerWeek + ";" + provisionRate + ";" + additionalAddressInfo + ";" + addressType + ";"
                        + gender + ";" + email + ";" + phoneNumber + "\n");

                // EMPLOYEE_EXTENSION_ID Zähler erhöhen
                employeeIdCounter++;
            }

            firstLine = true; // Rücksetzen für die zweite Datei

            employeeIdCounter = 1;
            while ((employeeOnlineshopBr.readLine()) != null) {
                if (firstLine) {
                    // Kopfzeile der EMPLOYEE CSV-Datei überspringen
                    firstLine = false;
                    continue;
                }

                // Zeile in EMPLOYEE_EXTENSION_ONLINESHOP CSV schreiben (ID + leere Felder)
                employeeOnlineshopWriter.write(employeeIdCounter + ";" + employeeIdCounter + ";;;;;;;;;\n");

                // EMPLOYEE_EXTENSION_ID Zähler erhöhen
                employeeIdCounter++;
            }

            System.out.println("Employee CSV Dateien wurden erfolgreich erstellt.");

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
