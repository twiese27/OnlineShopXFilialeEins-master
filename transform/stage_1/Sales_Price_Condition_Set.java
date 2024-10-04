import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.nio.file.Paths;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.io.FileWriter;

public class Sales_Price_Condition_Set {
    public static void main(String[] args) {
        String csvPrice = "dumps\\fi\\SALES_PRICE_CONDITION_SET.csv";
        String csvProductOS = "dumps\\os\\PRODUCT.csv";

        String outputCsvSalesPriceConditionSet = "transform\\stage_1\\transform_exports\\fi\\SALES_PRICE_CONDITION_SET.csv";


        // CSV-Daten in Listen von String-Arrays speichern
        List<String[]> csvDataPrice = readCSV(csvPrice, ";", 6);
        List<String[]> csvDataProductOS = readCSV(csvProductOS, ";", 14);

        //printCSVData(csvDataProductOS);

        createCSV(csvDataPrice, csvDataProductOS, outputCsvSalesPriceConditionSet);

    }

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

    private static void createCSV(List<String[]> csvDataPrice, List<String[]> csvDataProductsOS, String outputCsvFilePrice) {

        try (FileWriter writer = new FileWriter(outputCsvFilePrice)) {
            // Schreibe die Kopfzeile
            writer.append("SALES_PRICE_CONDITION_SET_ID; PRODUCT_ID; START_DATE; END_DATE; NETTO_PRICE; VAT_RATE\n");
            int idCounter = 1;

            for (String[] row : csvDataPrice) {
                String id = row[1];
                int productId = Integer.parseInt(id);
                int productIdNew = productId;
                String startDate = row[2];

                String dateForm = "yyyy-MM-dd";
                SimpleDateFormat simpleDateFormat = new SimpleDateFormat(dateForm);

                // Setze das Enddatum auf das heutige Datum
                Date today = new Date();
                String endDate = simpleDateFormat.format(today);

                String nettoPrice = row[4];
                String vatRate = row[5];
                String idCounterString = String.valueOf(idCounter);

                    writer.append(idCounterString).append(";");
                            if(productId == 0){
                                writer.append("0").append(";");
                            } else {
                                writer.append(String.valueOf(productIdNew)).append(";");
                            }
                            writer.append(startDate).append(";");

                            if(productId > 0 && productId < 1561 || idCounter == 17450 || idCounter == 17451){
                            writer.append(endDate).append(";");
                            } else {
                               writer.append(" ").append(";");
                            }

                            writer.append(nettoPrice).append(";")
                            .append(vatRate).append("\n");

                    idCounter++;
            }

            for(String[] row : csvDataPrice) {
                String id = row[1];
                int productId = Integer.parseInt(id);
                if(productId > 0 && productId < 1561) {
                    int productIdNew = productId;

                    String dateForm = "yyyy-MM-dd";
                    SimpleDateFormat simpleDateFormat = new SimpleDateFormat(dateForm);

                    // Setze das Enddatum auf das heutige Datum
                    Date today = new Date();

                    // +1 Tag zum heutigen Datum hinzufügen
                    Calendar calendar = Calendar.getInstance();
                    calendar.setTime(today);
                    calendar.add(Calendar.DAY_OF_MONTH, 1);
                    Date addedDate = calendar.getTime();

                    // Formatiere das neue Enddatum
                    String startDateNew = simpleDateFormat.format(addedDate);

                    String endDateNew = " ";
                    String nettoPriceNew = calculatePrice(csvDataProductsOS, productId);
                    String vatRateNew = "7.0";
                    String idCounterString = String.valueOf(idCounter);

                    writer.append(idCounterString).append(";")
                            .append(String.valueOf(productIdNew)).append(";")
                            .append(startDateNew).append(";")
                            .append(endDateNew).append(";")
                            .append(nettoPriceNew).append(";")
                            .append(vatRateNew).append("\n");

                    idCounter++;
                }
            }
            String dateForm = "yyyy-MM-dd";
            SimpleDateFormat simpleDateFormat = new SimpleDateFormat(dateForm);

            // Setze das Enddatum auf das heutige Datum
            Date today = new Date();

            // +1 Tag zum heutigen Datum hinzufügen
            Calendar calendar = Calendar.getInstance();
            calendar.setTime(today);
            calendar.add(Calendar.DAY_OF_MONTH, 1);
            Date addedDate = calendar.getTime();

            // Formatiere das neue Enddatum
            String startDateNew = simpleDateFormat.format(addedDate);

            writer.append(String.valueOf(idCounter)).append(";")
                    .append("17450").append(";")
                    .append(startDateNew).append(";")
                    .append(" ").append(";")
                    .append("399,99").append(";")
                    .append("7.0").append("\n");
            idCounter++;
            writer.append(String.valueOf(idCounter)).append(";")
                    .append("17451").append(";")
                    .append(startDateNew).append(";")
                    .append(" ").append(";")
                    .append("149,99").append(";")
                    .append("7.0").append("\n");

        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    private static String calculatePrice(List<String[]> csvDataProductsOS, Integer productId) {
        for(String[] row : csvDataProductsOS) {
            int id = Integer.parseInt(row[0]);
            if(id == productId-1) {
                double brutto = Double.parseDouble(row[4]);
                double vatrate = 7.0;
                double netto  = brutto / (1 + (vatrate/100));
                BigDecimal bd = new BigDecimal(netto);
                bd = bd.setScale(2, RoundingMode.HALF_UP);
                return bd.toString();
            }
        }

        return null;
    }

    private static Date addDays(Date date, int days)
    {
        Calendar cal = Calendar.getInstance();
        cal.setTime(date);
        cal.add(Calendar.DATE, days); //minus number would decrement the days
        return cal.getTime();
    }
}
