package com.paxata;

import com.paxata.custom.clustering.ClusterAlgorithm;
import com.paxata.custom.clustering.ClusterAlgorithmParam;
import org.apache.commons.codec.language.Metaphone;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.StringTokenizer;

public class AddressKeyGenerator implements ClusterAlgorithm {

    private static final long serialVersionUID = 5235721860418091129L;
    private List<ClusterAlgorithmParam> params;
    private static final String DESC_STRING = "Enable Nickname Flag";

    private static final String NAME_PAIRS_PATH = "com/paxata/namepairs.txt";
    private static final String NOISE_WORD_PATH = "com/paxata/address_noise.txt";


    public AddressKeyGenerator() {
        params = new ArrayList<>();
        ClusterAlgorithmParam stringParam = new ClusterAlgorithmParam(
				 /*displayName*/ DESC_STRING,
				 /*paramType*/
                ClusterAlgorithmParam.AlgoParamType.String,
				 /*paramValue*/ ""
        );
        params.add(stringParam);
    }

    @Override
    public String getDisplayName() {
        return "Multi Key Clustering function";
    }

    private volatile boolean initialized = false;
    private final Map<String, String> nicknameHashMap = new HashMap<>();
    private final List<String> delete_words_list = new ArrayList<>();


    @Override
    public String encode(String str) {
        init();
        StringBuffer sb = new StringBuffer();
        String[] str_arg = new String[] {str};
        str = str.toLowerCase().trim();
        String hash_value ="";
        String[] list_of_strings =str.split("\\W+");
        StringBuilder builder = new StringBuilder();
        StringBuilder output = new StringBuilder();
        Metaphone metaphone = new Metaphone();
        //DoubleMetaphone metaphone = new DoubleMetaphone();
        metaphone.setMaxCodeLen(7);
        Combinations combobj= new Combinations();
        //Permutations permobj= new Permutations();
        String[] outputarray = new String[list_of_strings.length];
        String[] tempoutputarray = new String[list_of_strings.length];

        //Part 1 - Replace any tokens that are abbreviations or nicknames
        for(int i=0;i< list_of_strings.length;i++){
            if (delete_words_list.contains(list_of_strings[i].toLowerCase().trim())) {
                list_of_strings[i] = "";
            }
            else{
                if (nicknameHashMap.containsKey(list_of_strings[i].toLowerCase().trim())) {
                    hash_value = nicknameHashMap.get(list_of_strings[i].toLowerCase().trim());
                    sb.append(hash_value +" ");
                }else {
                    // Remove any numbers also, may want to replace to the less harsh .replaceAll("[\\d.]", "");
                    sb.append(list_of_strings[i].replaceAll("[^A-Za-z]","") +" ");
                }
            }
        }
        // After name treatment, names might be multiple, so recalculate the length

        int new_length = sb.toString().trim().length();
        int frequency = new StringTokenizer(sb.toString().trim(), " ").countTokens();

        // Cater for the fact there might be single letter names
        if (frequency == 1) {
            outputarray[0]=sb.toString().trim();
        }
        else {
            if (frequency == 2) {
                //assuming I probably don't need this tempoutputarray, was just too lazy to figure out a better way
                tempoutputarray = sb.toString().trim().split(" ");
                outputarray[0] = tempoutputarray[0] + "," + tempoutputarray[1];
                outputarray[1] = tempoutputarray[1] + "," + tempoutputarray[0];
            }
            else if (frequency > 2) {
                str_arg[0] = sb.toString().trim();
                //Part 2 - Call the Combinations, to get various combinations in the event of multiple names (ie more than 2)
                sb = combobj.main(str_arg);
                //System.out.println(sb.toString());
                outputarray = sb.toString().trim().split(",");
            }
        }
        //flush the buffer
        sb.delete(0, sb.length());

        // The below should be configured differently to allow for different numbers of combos
        //for (int i = 0; i < outputarray.length; i++) {
        //    if (outputarray[i].length() - outputarray[i].replaceAll(" ", "").length() == 1) {
        //        //taking all the two length combinations for now
        //        sb.append(outputarray[i] + ",");
        //    }
        //}

        //Part 3 - Build the metaphone
        //maybe want to sort the list too?? (cater for word order)
        for (String string : outputarray) {
            if (string != null) {
                if (builder.length() != 0) {
                    builder.append("," + metaphone.encode(string));
                } else {
                    builder.append(metaphone.encode(string));
                }
            }
        }
        String values_to_metaphone = builder.toString();
        return values_to_metaphone;
    }

    private void init() {
        if (!initialized) {
            synchronized (nicknameHashMap) {
                BufferedReader br = null;
                try {
                    URL namepairsURL = getClass().getClassLoader().getResource(NAME_PAIRS_PATH);
                    URLConnection connection = namepairsURL.openConnection();
                    try (InputStream inputStream = connection.getInputStream()) {
                        br = new BufferedReader(new InputStreamReader(inputStream));
                        String sCurrentLine;
                        while ((sCurrentLine = br.readLine()) != null) {
                            int i = sCurrentLine.indexOf(',');
                            String nickname = sCurrentLine.substring(0, i).toLowerCase();
                            String fullname = sCurrentLine.substring(i + 1).toLowerCase();
                            nicknameHashMap.put(nickname, fullname);
                        }
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                } finally {
                    try {
                        if (br != null)
                            br.close();
                    } catch (IOException ex) {
                        ex.printStackTrace();
                    }
                }
            }
            synchronized (delete_words_list) {
                BufferedReader br = null;
                try {
                    URL namepairsURL = getClass().getClassLoader().getResource(NOISE_WORD_PATH);
                    URLConnection connection = namepairsURL.openConnection();
                    try (InputStream inputStream = connection.getInputStream()) {
                        br = new BufferedReader(new InputStreamReader(inputStream));
                        String sCurrentLine;
                        while ((sCurrentLine = br.readLine()) != null) {
                            delete_words_list.add(sCurrentLine.toLowerCase());
                        }
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                } finally {
                    try {
                        if (br != null)
                            br.close();
                    } catch (IOException ex) {
                        ex.printStackTrace();
                    }
                }
            }

            initialized = true;
        }
    }
    @Override
    public List<ClusterAlgorithmParam> getParams() {
        return params;
    }

}
