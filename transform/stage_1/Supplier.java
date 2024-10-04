import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

public class Supplier {

    public static void main(String[] args) {
        String sourceCsvFiliale = "dumps/fi/supplier_to_address_join.csv"; // Quell CSV-Datei für die Filiale
        String sourceCsvOnlineshop = "dumps/os/SUPPLIER.csv"; // Quell CSV-Datei für den Onlineshop
        String supplierFilialeCsv = "transform/stage_1/transform_exports/fi/SUPPLIER.csv"; // Ziel CSV-Datei für SUPPLIER_FILIALE
        String supplierExtensionFilialeCsv = "transform/stage_1/transform_exports/fi/SUPPLIER_EXTENSION.csv"; // Ziel CSV-Datei für SUPPLIER_EXTENSION_FILIALE
        String supplierExtensionOnlineshopCsv = "transform/stage_1/transform_exports/os/SUPPLIER_EXTENSION.csv"; // Ziel CSV-Datei für SUPPLIER_EXTENSION_ONLINESHOP

        // Zähler für SUPPLIER_EXTENSION_ID
        int supplierIdCounter = 1;

        try (BufferedReader br = new BufferedReader(new FileReader(sourceCsvFiliale));
             BufferedWriter supplierFilialeWriter = new BufferedWriter(new FileWriter(supplierFilialeCsv));
             BufferedWriter supplierExtensionWriter = new BufferedWriter(new FileWriter(supplierExtensionFilialeCsv));
             BufferedReader supplierBr = new BufferedReader(new FileReader(sourceCsvOnlineshop));
             BufferedWriter supplierOnlineshopWriter = new BufferedWriter(new FileWriter(supplierExtensionOnlineshopCsv))) {

            // Kopfzeilen für die Ziel-CSV-Dateien schreiben
            supplierFilialeWriter.write("SUPPLIER_ID;HOUSE_NUMBER;CITY;POSTAL_CODE;STREET;COUNTRY;NAME;IBAN;PHONE_NUMBER;CONTACT_PERSON;CONTACT_PERSON_EMAIL\n");
            supplierExtensionWriter.write("SUPPLIER_EXTENSION_ID;SUPPLIER_ID;ADDRESS_TYPE;ADDITIONAL_ADDRESS_INFORMATION\n");
            supplierOnlineshopWriter.write("SUPPLIER_EXTENSION_ID;SUPPLIER_ID;ADDRESS_TYPE;ADDITIONAL_ADDRESS_INFORMATION\n");

            String line;
            boolean firstLine = true;

            while ((line = br.readLine()) != null) {
                if (firstLine) {
                    // Kopfzeile der Quell CSV-Datei überspringen
                    firstLine = false;
                    continue;
                }

                // Spaltenwerte der Quell CSV-Datei aufteilen
                String[] values = line.split(";", -1);

                // SUPPLIER_FILIALE CSV füllen
                String houseNumber = values[11];
                String city = values[8];
                String postalCode = values[9];
                String street = values[10];
                String country = values[7].equals("Deutschland") ? "Germany" : values[7];
                String supplierName = values[1];
                String phoneNumber = values[3];
                String contactPerson = generateRandomName(); // Zufälligen Namen für die Kontaktperson generieren
                String contactPersonEmail = values[2];
                String iban = generateRandomIban(); // Random IBAN generieren

                // Zeile in SUPPLIER_FILIALE CSV schreiben
                supplierFilialeWriter.write(supplierIdCounter + ";" + houseNumber + ";" + city + ";" + postalCode + ";" + street + ";"
                        + country + ";" + supplierName + ";" + iban + ";" + phoneNumber + ";" + contactPerson + ";" + contactPersonEmail + "\n");

                // SUPPLIER_FILIALE_EXTENSION CSV füllen
                String addressType = values[13];
                String additionalAddressInfo = values[12];

                // Zeile in SUPPLIER_FILIALE_EXTENSION CSV schreiben
                supplierExtensionWriter.write(supplierIdCounter + ";" + supplierIdCounter + ";" + addressType + ";" + additionalAddressInfo + "\n");

                // SUPPLIER_EXTENSION_ID Zähler erhöhen
                supplierIdCounter++;
            }

            // Verarbeiten der dumps/os/SUPPLIER.csv Datei für SUPPLIER_EXTENSION_ONLINESHOP
            firstLine = true; // Rücksetzen für die zweite Datei

            supplierIdCounter = 1;
            while ((supplierBr.readLine()) != null) {
                if (firstLine) {
                    // Kopfzeile der SUPPLIER CSV-Datei überspringen
                    firstLine = false;
                    continue;
                }

                // Zeile in SUPPLIER_EXTENSION_ONLINESHOP CSV schreiben (ID + leere Felder)
                supplierOnlineshopWriter.write(supplierIdCounter + ";" + supplierIdCounter + ";;\n");

                // SUPPLIER_EXTENSION_ID Zähler erhöhen
                supplierIdCounter++;
            }

            System.out.println("Supplier CSV Dateien wurden erfolgreich erstellt.");

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Methode, um eine zufällige IBAN zu generieren
    private static String generateRandomIban() {
        String countryCode = "DE";
        String checkDigits = "89";
        String bankCode = "37040044";
        String accountNumber = String.format("%010d", (int) (Math.random() * 1000000000)); // Zufällige 10-stellige Kontonummer
        return countryCode + checkDigits + bankCode + accountNumber;
    }

    // Methode, um einen zufälligen Namen zu generieren
    private static String generateRandomName() {
        String[] firstNames = {"Hans", "Peter", "Anna", "Laura", "Michael", "Sabine", "Klaus", "Julia", "Markus", "Lena"};
        String[] lastNames = {"Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Hoffmann", "Schulz"};

        Random random = new Random();
        String firstName = firstNames[random.nextInt(firstNames.length)];
        String lastName = lastNames[random.nextInt(lastNames.length)];

        return firstName + " " + lastName;
    }
}