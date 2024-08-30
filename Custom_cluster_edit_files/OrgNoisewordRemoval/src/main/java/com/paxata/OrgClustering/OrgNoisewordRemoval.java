package com.paxata.OrgClustering;

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
import java.util.List;
import java.util.Collections;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.Comparator;

public class OrgNoisewordRemoval implements ClusterAlgorithm {

    private static final long serialVersionUID = 5235721860418091128L;
    private List<ClusterAlgorithmParam> params;
    private static final String DESC_STRING = "Enable Nickname Flag";

    private static final String ORG_DELETE_WORDS_PATH = "com/paxata/OrgClustering/org_delete_tokens.txt";

    public OrgNoisewordRemoval() {
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
        return "Org Clustering function";
    }

    private volatile boolean initialized = false;
    private final List<String> delete_words_list = new ArrayList<>();


    @Override
    public String encode(String str) {
        init();
        String regex = "";
        String cleaned_string = "";
        StringBuffer sb = new StringBuffer();

        //Remove strange word boundary characters.. probably unnecessary
        String[] list_of_strings =str.split("\\W+");
        StringBuilder builder = new StringBuilder(" ");
        for(int i=0;i< list_of_strings.length;i++){
            builder.append(list_of_strings[i].trim()+ " ");
        }
        str = builder.toString().trim();
        //sort the list of noise words from longest to shortest
        SortListByLength(delete_words_list);

        //cycle through the List deleting any matching tokens from the input string
        for (int i=0; i < delete_words_list.size();i++ ){
            regex = "\\b"+delete_words_list.get(i)+"\\b";
            sb = replace_noise_words(str,regex,"");
            str = sb.toString();
        }
        cleaned_string = sb.toString().trim().replaceAll(" +", " ");
        return cleaned_string;
    }


    public String replace_noise_words_alternative(String input, String regex, String replacement) {
        Pattern p = Pattern.compile(regex, Pattern.CASE_INSENSITIVE);
        Matcher m = p.matcher(input);
        String result = m.replaceAll(replacement);
        return result;
    }

    public StringBuffer replace_noise_words(String input,String regex,String replacement){
        Pattern p = Pattern.compile(regex,Pattern.CASE_INSENSITIVE);
        Matcher m = p.matcher(input);
        StringBuffer sb = new StringBuffer();
        boolean result = m.find();
        while (result)
        {
            m.appendReplacement(sb, replacement);
            result = m.find();
        }
        m.appendTail(sb);
        return sb;
    }

    //This is to sort the list by length which is quite important (to look for the longest Strings first so the
    // replacement rules don't mess with each other
    public void SortListByLength(List delete_words_list){
        Comparator<String> stringLengthComparator = new Comparator<String>() {
            @Override
            public int compare(String o1, String o2) {
                return Integer.compare(o1.length(), o2.length());
            }
        };
        Collections.sort(delete_words_list,Collections.reverseOrder());
    }

    private void init() {
        if (!initialized) {
            synchronized (delete_words_list) {
                BufferedReader br = null;
                try {

                    URL namepairsURL = getClass().getClassLoader().getResource(ORG_DELETE_WORDS_PATH);
                    URLConnection connection = namepairsURL.openConnection();
                    try (InputStream inputStream = connection.getInputStream()) {
                        br = new BufferedReader(new InputStreamReader(inputStream));
                        String sCurrentLine;
                        while ((sCurrentLine = br.readLine()) != null) {
                            delete_words_list.add(sCurrentLine);
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