package com.paxata;

import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;
import org.junit.Assert;

/**
 * Unit test for simple App.
 */
public class MultiKeyGeneratorTest {
    @org.junit.Test
    public void Bill_nicknameFor_William() {
        Assert.assertEquals("SM0RBRT,WLMRBRT,WLMSM0", encode("Bill Smith Bob"));
        Assert.assertEquals("WLM", encode("WILLIAM"));
    }

    @org.junit.Test
    public void Bob_Rob_Bobby_and_Robert() {
        Assert.assertEquals("RBRTSM0,SM0RBRT", encode("  Bob Smith"));
        Assert.assertEquals("RBRT", encode("Rob  "));
        Assert.assertEquals("RBRT", encode("Bobby"));
    }

    @org.junit.Test
    public void Longer_names() {
        Assert.assertEquals("RBRTSM0,SM0RBRT", encode("Bob Smith"));
    }


    @org.junit.Test
    public void Multiword_test() {
        Assert.assertEquals("MYRSSKB,BRSTLSK,BRSTLMY", encode("  BMS "));

        Assert.assertEquals("MYRSSKB,BRSTLSK,BRSTLMY", encode("Bristol Myers Squibb  "));
    }


    private String encode(String name) {
        return new MultiKeyGenerator().encode(name);
    }
}
