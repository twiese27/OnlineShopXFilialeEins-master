import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.io.FileWriter;

public class product {
    public static void main(String[] args) {
        String csvProduct = "dumps\\fi\\PRODUCT.csv";  // Pfad zur ersten CSV-Datei
        String csvPriceSet = "dumps\\fi\\SALES_PRICE_CONDITION_SET.csv";
        String csvPackage = "dumps\\fi\\PACKAGE.csv";
        String csvProductAlt = "transform\\stage_1\\produkte_alt_filiale.csv";
        String csvProducerNeu = "transform\\stage_1\\transform_exports\\fi\\PRODUCER.csv";


        //String outputCsvProduct = "PRODUCT_FILIALE.csv";
        String outputCsvProduct = "transform\\stage_1\\transform_exports\\fi\\PRODUCT.csv";


        // CSV-Daten in Listen von String-Arrays speichern
        List<String[]> csvDataProduct = readCSV(csvProduct, ";", 12);
        List<String[]> csvDataPriceSet = readCSV(csvPriceSet, ";", 6);
        List<String[]> csvDataPackage = readCSV(csvPackage, ";", 5);
        List<String[]> csvDataProductAlt = readCSV(csvProductAlt, ";", 15);
        List<String[]> csvDataProducerNeu = readCSV(csvProducerNeu, ";", 7);


        createCSV(csvDataProduct,csvDataPackage, csvDataPriceSet, csvDataProductAlt, csvDataProducerNeu, outputCsvProduct);

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


    private static void createCSV(List<String[]> csvDataProduct, List<String[]> csvDataPackage,
                                 List<String[]> csvDataPrice, List<String[]> csvDataProductAlt , List<String[]> csvDataProducerNeu,
                                  String outputCsvFileProduct) {


        try (FileWriter writer = new FileWriter(outputCsvFileProduct)) {
            // Schreibe die Kopfzeile
            writer.append("PRODUCT_ID; CASES_PER_PALLET; UNITS_PER_CASE; PRODUCT_NAME; SRP; RECYCABLAE_PACKAGE; LOW_FAT; RETAIL_PRICE;" +
                    "GROSS_WEIGHT; SHELF_WIDTH; PRODUCER_ID; SKU; PRODUCT_CATEGORY_ID; NET_WEIGHT\n");

            for (String[] row : csvDataProduct) {
                String id = row[0]; // Product ID in String-Form
                int productId = Integer.parseInt(id);

                if (productId == 0 || productId > 1560){
                    String unitsPerCase = row[9];
                    String prodcutName = row[5];
                    String srpString = getPrice(csvDataPrice,id);
                    int packageId = Integer.parseInt(String.valueOf(row[11]));
                    String recycablePackage = getRecycablePackage(csvDataPackage, packageId);
                    String casesPerPallet = getCasesPerPallet(csvDataProductAlt, id);
                    String lowFat = row[10];
                    String grossWeight = row[6];
                    String shelfWidth = getShelfWidth(csvDataPackage, packageId);
                    String sku = row[3];
                    String productCategoryId = row[2];
                    String netWeight = row[7];
                    String producerName = row[4];
                    String producerId = getProducerId(csvDataProducerNeu, producerName);

                    writer.append(id).append(";")
                            .append(casesPerPallet).append(";")
                            .append(unitsPerCase).append(";")
                            .append(prodcutName).append(";")
                            .append(srpString).append(";")
                            .append(recycablePackage).append(";")
                            .append(lowFat).append(";")
                            .append(srpString).append(";")
                            .append(grossWeight).append(";")
                            .append(shelfWidth).append(";")
                            .append(producerId).append(";")
                            .append(sku).append(";")
                            .append(productCategoryId).append(";")
                            .append(netWeight).append("\n");
                }

            }

        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private static String getProducerId(List<String[]> csvDataProducerNeu, String producerName) {
        for(String[] row : csvDataProducerNeu) {
            if (row[5].equals(producerName)) {
                return row[0];
            }
        }
        return null;
    }


    private static String getCasesPerPallet(List<String[]> csvDataProductAlt, String id) {
        String idString = String.valueOf(Integer.parseInt(id));
        for(String[] row : csvDataProductAlt){
            if(idString.equals(row[1])){
                return row[11];
            }
        }
        return null;
    }

    private static String getPrice(List<String[]> csvDataPrice, String id) {
        for (String[] row : csvDataPrice) {
            if (id.equals(row[1])) {
                double basePrice = Double.parseDouble(row[4]);
                double adjustment = Double.parseDouble(row[5]);
                double finalPrice;

                // Special handling for ID 17450 or 17451
                if (id.equals("17450") || id.equals("17451")) {
                    finalPrice = (basePrice + (basePrice / 100 * adjustment)) / 10;
                } else {
                    finalPrice = basePrice + (basePrice / 100 * adjustment);
                }

                return String.format("%.2f", finalPrice);
            }
        }
        return null;
    }


    private static String getShelfWidth(List<String[]> data, int packageId) {
        String packageIdString = String.valueOf(packageId); // Konvertiere packageId in einen String
        for (String[] row : data) {
            if (row[0].equals(packageIdString)) { // Vergleiche Strings
                return row[2];
            }
        }
        return null;
    }


    private static String getRecycablePackage(List<String[]> data, int packageId) {
        String packageIdString = String.valueOf(packageId); // Konvertiere packageId in einen String
        for(String[] row : data) {
            if(row[0].equals(packageIdString)){
                return row[4];
            }
        }
        return null;
    }


}
