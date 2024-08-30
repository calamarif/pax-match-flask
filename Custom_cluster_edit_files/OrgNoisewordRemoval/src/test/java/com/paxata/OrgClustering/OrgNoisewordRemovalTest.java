package com.paxata.OrgClustering;


import org.junit.Test;
import org.junit.Assert;

public class OrgNoisewordRemovalTest {
    @org.junit.Test
    public void LTD_Removal() {
        Assert.assertEquals("Callum REALTD Calamari", encode("Callum PTY   REALTD Calamari "));
    }

    @org.junit.Test
    public void lowercase_Removal() {
        Assert.assertEquals("A THOMAS Parsa MD", encode("A.THOMAS Parsa INC MD INC "));
    }

    @org.junit.Test
    public void multitokennoise_Removal() {
        Assert.assertEquals("A Thomas Parsa", encode("A.Thomas Parsa AGENCY MEDICAL DOCTORS PROFESSIONAL ASSN\n"));
        Assert.assertEquals("Calamari", encode("Calamari CREDIT UNION"));
    }



        private String encode(String name) {
        return new OrgNoisewordRemoval().encode(name);
    }
}
