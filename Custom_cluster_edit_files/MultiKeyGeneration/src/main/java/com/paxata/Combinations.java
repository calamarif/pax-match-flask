package com.paxata;

/**
 * Created by callumfinlayson on 11/10/17.
class is expecting a comma separated list of tokens to create combinations of
 */
public class Combinations {

    public static StringBuffer main (String[] args){
        //String[] str_arg = new String[] {"Callum David Finlayson Steve"};
        StringBuffer sb = new StringBuffer();
        sb = Combinations(args[0],sb);
        return sb;
    }

    public static void buildNameChoicesHelper(String[] nameArray, StringBuffer sb , int nameIndex,
                                              String str) {
        if (nameIndex >= nameArray.length) {
            if (str.length() > 0) {
                //Commenting out the below debug line
                //System.out.println(str.substring(0, str.length() - 1));
                sb.append(str.substring(0, str.length() - 1) + ",");
            }
        } else {
            buildNameChoicesHelper(nameArray, sb,nameIndex + 1, str);
            buildNameChoicesHelper(nameArray, sb,nameIndex + 1, str + nameArray[nameIndex] + " ");
        }
    }

    public static StringBuffer Combinations(String nameStr, StringBuffer sb) {
        String[] nameArray = nameStr.split("\\W", -1);
        buildNameChoicesHelper(nameArray, sb, 0, "");
        //split the StringBuffer into multiple elements in array
        String[] outputarray = sb.toString().split(",");
        sb.delete(0,sb.length());

        for (int i = 0; i < outputarray.length; i++){
            // The below if statement should be configured differently to allow for different numbers of combos
            if (outputarray[i].length() - outputarray[i].replaceAll(" ", "").length()==1) {
                //taking all the two length combinations for now
                //System.out.println("> "+outputarray[i]);
                sb.append(outputarray[i]+",");
            }
        }
        return sb;
    }
}