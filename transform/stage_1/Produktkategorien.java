import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.io.FileWriter;
import java.util.Map;


public class Produktkategorien {

    public static void main(String[] args) {
        String csvFile1 = "C:\\Users\\carag\\Desktop\\Daten BI\\fililae.csv";  // TODO: Noch einfügen
        String csvFile2 = "C:\\Users\\carag\\Desktop\\Daten BI\\onlineshop.csv";  // TODO: Noch einfügen
        String csvSplitBy = ",";
        String outputCsvFile = "vergleich.csv";

        // CSV-Daten in Listen von String-Arrays speichern
        List<String[]> csvData1 = readCSV(csvFile1, csvSplitBy, 4);
        List<String[]> csvData2 = readCSV(csvFile2, csvSplitBy, 3);

        //printCSVData(csvData1);
        //printCSVData(csvData2);

        compareAndWriteCSV(csvData1, csvData2, outputCsvFile);

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

    // Funktion zum Einlesen einer CSV-Datei und Speichern in einer Liste von Arrays
    public static List<String[]> readCSV(String csvFile, String csvSplitBy) {
        List<String[]> csvData = new ArrayList<>();
        String line;

        try (BufferedReader br = new BufferedReader(new FileReader(csvFile))) {
            br.readLine();  // Kopfzeile überspringen

            // Zeilenweise durch die Datei iterieren
            while ((line = br.readLine()) != null) {
                // Zeile in Spalten aufteilen, auch leere Werte beachten
                String[] spalten = line.split(csvSplitBy, -1);  // '-1' sorgt dafür, dass auch leere Felder berücksichtigt werden
                if (spalten.length >= 3) {
                    csvData.add(spalten);  // Füge das Array der Liste hinzu
                } else {
                    System.out.println("Ungültige Anzahl von Spalten: " + spalten.length);
                }
            }

        } catch (IOException e) {
            e.printStackTrace();
        }

        return csvData;
    }

    // Funktion zum Vergleichen der CSV-Daten und Schreiben der Ergebnisse in eine neue CSV-Datei
    private static void compareAndWriteCSV(List<String[]> csvData1, List<String[]> csvData2, String outputCsvFile) {
        // Erstelle eine Map für die Daten der zweiten CSV-Datei (basierend auf Namen)
        Map<String, String[]> csvData2Map = new HashMap<>();
        for (String[] row : csvData2) {
            if (row.length >= 3) {
                String nameOS = row[1];  // Name_OS
                csvData2Map.put(nameOS, row);
            }
        }

        // Erstelle eine Map für die Daten der ersten CSV-Datei (basierend auf Namen)
        Map<String, String[]> csvData1Map = new HashMap<>();
        for (String[] row : csvData1) {
            if (row.length >= 3) {
                String nameFI = row[2];  // Name_FI
                csvData1Map.put(nameFI, row);
            }
        }

        try (FileWriter writer = new FileWriter(outputCsvFile)) {
            // Schreibe die Kopfzeile
            writer.append("Hierachy_Level,ID_FI,TopID_FI,Name_FI,ID_OS,TopID_OS,Name_OS\n");

            // Zuerst: Vergleiche jede Zeile aus der ersten Liste mit der Map der zweiten Liste
            for (String[] row1 : csvData1) {
                if (row1.length >= 4) {
                    String idFI = row1[0];           // ID_FI
                    String topIdFI = row1[1];        // TopID_FI
                    String topIdNameFI = findName1(csvData1,topIdFI);
                    String nameFI = row1[2];         // Name_FI
                    String hierachyLevel = row1[3];  // Hierachy_Level

                    // Suche nach einem passenden Namen in der Map der zweiten Datei
                    String[] matchingRow = csvData2Map.get(nameFI);

                    if (matchingRow != null) {
                        // Wenn ein Match gefunden wurde, schreibe die Daten in die Ausgabedatei
                        String idOS = matchingRow[0];    // ID_OS
                        String topIdOS = matchingRow[2];  // TopID_OS
                        String topIdNameOS = findName2(csvData2,topIdOS);

                        writer.append(hierachyLevel).append(",")
                                .append(idFI).append(",")
                                .append(topIdFI).append(" (").append(topIdNameFI).append("),")
                                .append(nameFI).append(",")
                                .append(idOS).append(",")
                                .append(topIdOS).append(" (").append(topIdNameOS).append("),")
                                .append(nameFI).append("\n");


                        // Entferne das passende Element aus der zweiten Map, um doppelte Einträge zu vermeiden
                        csvData2Map.remove(nameFI);
                    } else {
                        // Wenn kein Match gefunden wurde, schreibe nur die Daten der ersten CSV-Datei
                        writer.append(hierachyLevel).append(",")
                                .append(idFI).append(",")
                                .append(topIdFI).append(" (").append(topIdNameFI).append("),")
                                .append(nameFI).append(",")
                                .append(",,")   // Leere Felder für die zweite CSV-Datei
                                .append("\n");
                    }
                }
            }

            // Dann: Schreibe die restlichen Zeilen aus der zweiten CSV-Datei, die keinen Match gefunden haben
            for (String[] row2 : csvData2Map.values()) {
                if (row2.length >= 3) {
                    String idOS = row2[0];      // ID_OS
                    String topIdOS = row2[2];   // TopID_OS
                    String topIdNameOS = findName2(csvData2,topIdOS);
                    String nameOS = row2[1];    // Name_OS

                    writer.append(",,,")          // Leere Felder für die erste CSV-Datei
                            .append(idOS).append(",")
                            .append(topIdOS).append(" (").append(topIdNameOS).append("),")
                            .append(nameOS).append("\n");
                }
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static String findName2(List<String[]> csvData, String Id) {
        String name;
        for(String[] row : csvData) {
            if(row[0].equals(Id)) {
                name = row[1];
                return name;
            }
        }
        return null;
    }

    private static String findName1(List<String[]> csvData, String Id) {
        String name;
        for(String[] row : csvData) {
            if(row[0].equals(Id)) {
                name = row[2];
                return name;
            }
        }
        return null;
    }
}