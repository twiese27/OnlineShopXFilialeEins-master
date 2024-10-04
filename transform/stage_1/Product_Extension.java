import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.io.FileWriter;

public class Product_Extension {
    public static void main(String[] args) {
        String csvProduct = "dumps\\fi\\PRODUCT.csv";  // Pfad zur ersten CSV-Datei
        String csvProductOS = "dumps\\os\\PRODUCT.csv";
        String csvPackage = "dumps\\fi\\PACKAGE.csv";


        //String outputCsvProductExtension_FI = "PRODUCT_EXTENSION_FILIALE.csv";
        String outputCsvProductExtension_FI = "transform\\stage_1\\transform_exports\\fi\\PRODUCT_EXTENSION.csv";
        //String outputCsvProductExtension_OS = "PRODUCT_EXTENSION_ONLINESHOP.csv";
        String outputCsvProductExtension_OS = "transform\\stage_1\\transform_exports\\os\\PRODUCT_EXTENSION.csv";


        // CSV-Daten in Listen von String-Arrays speichern
        List<String[]> csvDataProduct = readCSV(csvProduct, ";", 12);
        List<String[]> csvDataProductOS = readCSV(csvProductOS, ";", 14);
        List<String[]> csvDataPackage = readCSV(csvPackage, ";", 5);


        createCSV(csvDataProduct, csvDataPackage, csvDataProductOS, outputCsvProductExtension_FI, outputCsvProductExtension_OS);

    }

    // Funktion zum Einlesen einer CSV-Datei und Speichern in einer Liste von Arrays
    private static List<String[]> readCSV(String csvFile, String csvSplitBy, Integer spaltenanzahl) {
        List<String[]> csvData = new ArrayList<>();
        String line;

        try (BufferedReader br = new BufferedReader(new FileReader(csvFile))) {
            br.readLine();  // Kopfzeile überspringen

            // Zeilenweise durch die Datei iterieren
            while ((line = br.readLine()) != null) {
                // Zeile in Spalten aufteilen, auch leere Werte beachten
                String[] spalten = line.split(csvSplitBy, -1);  // '-1' sorgt dafür, dass auch leere Felder berücksichtigt werden
                if (spalten.length == spaltenanzahl) {
                    csvData.add(spalten);  // Füge das Array mit 4 Spalten der Liste hinzu
                } else {
                    System.out.println("Ungültige Anzahl von Spalten: " + spalten.length);
                }
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
        return csvData;
    }


    private static void createCSV(List<String[]> csvDataProduct, List<String[]> csvDataPackage, List<String[]> csvDataProductOS,
                                 String outputCsvFileProduct, String outputCsvFileProductOS) {

        //Product_Extension Filiale
        try (FileWriter writer = new FileWriter(outputCsvFileProduct)) {
            // Schreibe die Kopfzeile
            writer.append("PRODUCT_EXTENSION_ID; PRODUCT_ID; SHELF_HEIGHT; SHELF_DEPTH\n");
            int idCounter = 1;

            for (String[] row : csvDataProduct) {
                String id = row[0]; // Product ID in String-Form
                int productId = Integer.parseInt(id);
                String packageId = row[11];
                int packageIdInt = Integer.parseInt(packageId);


                    String idCounterString = String.valueOf(idCounter);
                    String shelfHeight = getShelfInfo(csvDataPackage, packageIdInt, 3);
                    String shelfDepth = getShelfInfo(csvDataPackage, packageIdInt, 1);

                    writer.append(idCounterString).append(";")
                            .append(id).append(";")
                            .append(shelfHeight).append(";")
                            .append(shelfDepth).append("\n");

                    idCounter++;
            }

        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        //Product_Extension Onlineshop
        try (FileWriter writer = new FileWriter(outputCsvFileProductOS)) {
            // Schreibe die Kopfzeile
            writer.append("PRODUCT_EXTENSION_ID; PRODUCT_ID; SHELF_HEIGHT; SHELF_DEPTH\n");
            int idCounter = 1;

            for (String[] row : csvDataProductOS) {
                String id = row[0]; // Product ID in String-Form


                    String idCounterString = String.valueOf(idCounter);

                    writer.append(idCounterString).append(";")
                            .append(id).append(";")
                            .append(" ").append(";")
                            .append(" ").append("\n");

                    idCounter++;


                }

        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private static String getShelfInfo(List<String[]> data, int packageId, int index) {
        String packageIdString = String.valueOf(packageId); // Konvertiere packageId in einen String
        for (String[] row : data) {
            if (row[0].equals(packageIdString)) { // Vergleiche Strings
                return row[index];
            }
        }
        return null;
    }
}
