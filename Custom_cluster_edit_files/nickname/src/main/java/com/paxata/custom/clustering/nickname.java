package com.paxata.custom.clustering;

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

public class nickname  implements ClusterAlgorithm {

    private static final long serialVersionUID = 5235721860418091129L;
    private List<ClusterAlgorithmParam> params;
    private static final String DESC_STRING = "Enable Nickname Flag";

    private static final String NAME_PAIRS_PATH = "com/paxata/custom/clustering/namepairs.txt";

    public nickname() {
        params = new ArrayList<>();
        ClusterAlgorithmParam stringParam = new ClusterAlgorithmParam(
				 /*displayName*/ DESC_STRING,
				 /*paramType*/
                ClusterAlgorithmParam.AlgoParamType.String,
				 /*paramValue*/ "" );
        params.add(stringParam);
    }

    @Override
    public String getDisplayName() {
        return "Nickname Clustering function";
    }

    private volatile boolean initialized = false;
    private final Map<String, String> nicknameHashMap = new HashMap<>();

    @Override
    public String encode(String str) {
        init();
        if (nicknameHashMap.containsKey(str.toLowerCase())) {
            str = nicknameHashMap.get(str.toLowerCase());
        }
        Metaphone metaphone = new Metaphone();
        return metaphone.encode(str);
    }

    private void init() {
        if (!initialized) {
            synchronized (nicknameHashMap) {
                BufferedReader br = null;
                try {
                    URL namepairsURL = getClass().getClassLoader().getResource(NAME_PAIRS_PATH);
                    URLConnection connection = namepairsURL.openConnection();
                    try(InputStream inputStream = connection.getInputStream()) {
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
            initialized = true;
        }
    }

    @Override
    public List<ClusterAlgorithmParam> getParams() {
        return params;
    }

}
