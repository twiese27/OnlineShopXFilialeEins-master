import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.security.Timestamp;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.List;
import java.io.FileWriter;


public class Shopping_Order_Cart {

    public static void main(String[] args) {
        String csvPurchase = "dumps\\fi\\PURCHASE.csv";  // Pfad zur ersten CSV-Datei
        String csvShoppingCart = "dumps\\os\\SHOPPING_CART.csv";
        String csvShoppingOrder = "dumps\\os\\SHOPPING_ORDER.csv";

        //String outputCsvFileOrder = "SHOPPING_ORDER_FILIALE.csv";
        String outputCsvFileOrder = "transform\\stage_1\\transform_exports\\fi\\SHOPPING_ORDER.csv";
        //String outputCsvFileCart = "SHOPPING_CART_FILIALE.csv";
        String outputCsvFileCart = "transform\\stage_1\\transform_exports\\fi\\SHOPPING_CART.csv";
        //String outputCsvFileCartExtension_FI = "SHOPPING_CART_EXTENSION_FILIALE.csv";
        String outputCsvFileCartExtension_FI = "transform\\stage_1\\transform_exports\\fi\\SHOPPING_CART_EXTENSION.csv";
        //String outputCsvFileCartExtension_OS = "SHOPPING_CART_EXTENSION_ONLINESHOP.csv";
        String outputCsvFileCartExtension_OS = "transform\\stage_1\\transform_exports\\os\\SHOPPING_CART_EXTENSION.csv";
        //String outputCsvFileOrderExtension_FI = "SHOPPING_ORDER_EXTENSION_FILIALE.csv";
        String outputCsvFileOrderExtension_FI = "transform\\stage_1\\transform_exports\\os\\SHOPPING_ORDER_EXTENSION.csv";
        //String outputCsvFileOrderExtension_OS = "SHOPPING_ORDER_EXTENSION_ONLINESHOP.csv";
        String outputCsvFileOrderExtension_OS = "transform\\stage_1\\transform_exports\\os\\SHOPPING_ORDER_EXTENSION.csv";

        // CSV-Daten in Listen von String-Arrays speichern
        List<String[]> csvData1 = readCSV(csvPurchase, ",", 10);
        List<String[]> csvDataCart = readCSV(csvShoppingCart, ";", 5);
        List<String[]> csvDataOrder = readCSV(csvShoppingOrder, ";", 7);

        //printCSVData(csvData1);

        createCSV(csvData1, csvDataCart, csvDataOrder, outputCsvFileOrder, outputCsvFileCart, outputCsvFileCartExtension_FI, outputCsvFileCartExtension_OS,
                outputCsvFileOrderExtension_FI, outputCsvFileOrderExtension_OS);

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

    // Funktion zur Ausgabe der CSV-Daten
    private static void printCSVData(List<String[]> csvData) {
        for (String[] row : csvData) {
            // Ausgabe jedes Arrays als kommagetrennte Werte
            System.out.println(String.join(", ", row));
        }
    }



    private static void createCSV(List<String[]> csvData1, List<String[]> csvDataCart, List<String[]> CSVDataOder,
                                 String outputCsvFile1, String outputCsvFile2, String outputCsvExtensionCart_FI, String outputCsvExtensionCart_OS,
                                 String outputCsvExtensionOrder_FI, String outputCsvExtensionOrder_OS) {

        //Shopping Order
        try (FileWriter writer = new FileWriter(outputCsvFile1)) {
            // Schreibe die Kopfzeile
            writer.append("ORDER_ID; STATUS; ORDER_TIME; SHOPPING_CART_ID; EMPLOYEE_ID; DELIVERY_SERVICE_ID; TOTAL_PRICE\n");

            int idCounter = 1;
            for(String[] row : csvData1) {
                String orderId = row[0];        //Order_Id
                String status = "delivered";   //Status
                String orderTime = row[4];     // Order_Time
                String totalPrice = row[5];    //Total_Price
                String employeeId = row[2];     //Employee_Id
                String idCounterString = String.valueOf(idCounter);

                writer.append(orderId).append(";")
                        .append(status).append(";")
                        .append(orderTime).append(";")
                        .append(idCounterString).append(";")
                        .append(employeeId).append(";")
                        .append(" ").append(";")
                        .append(totalPrice).append("\n");
                idCounter++;
            }


        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        //Shopping Cart
        try (FileWriter writer = new FileWriter(outputCsvFile2)) {
            // Schreibe die Kopfzeile
            writer.append("SHOPPING_CART_ID; DELETED_ON; CREATED_ON; AMOUNT_OF_PRODUCTS; CUSTOMER_ID\n");

            int idCounter = 1;

            for(String[] row : csvData1) {
                String timestampString = row[4];  // Hier steht der Timestamp

                String datePartString = extractDateFromTimestamp(timestampString);

                String amountOfProducts = row[9];    //Amount_Of_Products
                String customerId = row[3];        //Customer_Id
                String idCounterString = String.valueOf(idCounter);

                writer.append(idCounterString).append(";")
                        .append(" ").append(";")
                        .append(datePartString).append(";")
                        .append(amountOfProducts).append(";")
                        .append(customerId).append("\n");
                idCounter++;
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }


        //Shopping Cart Extension_Filiale
        try (FileWriter writer = new FileWriter(outputCsvExtensionCart_FI)) {
            // Schreibe die Kopfzeile
            writer.append("SHOPPING_CART_EXTENSION_ID; SHOPPING_CART_ID; POINT_OF_SALE_ID\n");

            int idCounter = 1;

            for(String[] row : csvData1) {

                String idCounterString = String.valueOf(idCounter);

                writer.append(idCounterString).append(";")
                        .append(idCounterString).append(";")
                        .append("1").append("\n");
                idCounter++;
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        //Shopping Cart Extension_Onlineshop
        try (FileWriter writer = new FileWriter(outputCsvExtensionCart_OS)) {
            // Schreibe die Kopfzeile
            writer.append("SHOPPING_CART_EXTENSION_ID; SHOPPING_CART_ID; POINT_OF_SALE_ID\n");

            int idCounter = 1;

            for(String[] row : csvDataCart) {

                String idCounterString = String.valueOf(idCounter);

                writer.append(idCounterString).append(";")
                        .append(idCounterString).append(";")
                        .append("2").append("\n");
                idCounter++;
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        //Shopping Order Extension_Filiale
        try (FileWriter writer = new FileWriter(outputCsvExtensionOrder_FI)) {
            // Schreibe die Kopfzeile
            writer.append("SHOPPING_ORDER_EXTENSION_ID; ORDER_ID; NET_PURCHASE_PRICE; POINT_OF_SALE_ID; CASH_REGISTRY_ID\n");

            int idCounter = 1;

            for(String[] row : csvData1) {

                String idCounterString = String.valueOf(idCounter);
                String netPurchasePrice = row[6];
                String cashRegistryId = row[1];

                writer.append(idCounterString).append(";")
                        .append(idCounterString).append(";")
                        .append(netPurchasePrice).append(";")
                        .append("1").append(";")
                        .append(cashRegistryId).append("\n");
                idCounter++;
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        //Shopping Cart Extension_Onlineshop
        try (FileWriter writer = new FileWriter(outputCsvExtensionOrder_OS)) {
            // Schreibe die Kopfzeile
            writer.append("SHOPPING_ORDER_EXTENSION_ID; ORDER_ID; NET_PURCHASE_PRICE; POINT_OF_SALE_ID; CASH_REGISTRY_ID\n");

            int idCounter = 1;

            for(String[] row : csvDataCart) {

                String idCounterString = String.valueOf(idCounter);

                writer.append(idCounterString).append(";")
                        .append(idCounterString).append(";")
                        .append(" ").append(";")
                        .append("2").append(";")
                        .append(" ").append("\n");
                idCounter++;
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }



    private static String extractDateFromTimestamp(String timestampString) {
        // Erstelle zwei mögliche DateTimeFormatter
        DateTimeFormatter formatterWithMillis = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSSSSS");
        DateTimeFormatter formatterWithoutMillis = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

        LocalDateTime timestamp = null;

        // Versuche zuerst, mit Millisekunden zu parsen
        try {
            if (timestampString.contains(".")) {
                timestamp = LocalDateTime.parse(timestampString, formatterWithMillis);
            } else {
                timestamp = LocalDateTime.parse(timestampString, formatterWithoutMillis);
            }
        } catch (DateTimeParseException e) {
            // Falls ein Parsing-Fehler auftritt, gib eine Fehlermeldung aus und setze das Datum auf "N/A"
            System.out.println("Ungültiger Timestamp: " + timestampString);
            return "N/A";
        }

        // Extrahiere nur den Datumsteil (LocalDate) und gib ihn als String zurück
        LocalDate datePart = timestamp.toLocalDate();
        return datePart.toString();
    }
}
