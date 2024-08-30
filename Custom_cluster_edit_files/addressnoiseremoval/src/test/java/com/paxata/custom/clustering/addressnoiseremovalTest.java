package com.paxata.custom.clustering;

import static org.junit.Assert.assertTrue;

import org.junit.Assert;
import org.junit.Test;

/**
 * Unit test for simple addressnoiseremoval.
 */

/**
 * Created by callumfinlayson on 8/20/20.
 */
public class addressnoiseremovalTest {

    /**
     * Unit test for simple App.
     */
    @org.junit.Test
    public void Bill_nicknameFor_William() {
        Assert.assertEquals("1 Main Something", encode("1 Main Something st"));
        Assert.assertEquals("1 Main brother", encode("1 Main brother st"));
    }

    @org.junit.Test
    public void Bob_Rob_Bobby_and_Robert() {
        Assert.assertEquals("15 32B Wattletree", encode("Unit 15 , 32B Wattletree Road"));
        Assert.assertEquals("WATTLETREE Toorak Glenferie", encode("WATTLETREE Toorak Glenferie ROAD  "));
        Assert.assertEquals("WATTLETREE Glenferie Toorak", encode("WATTLETREE Glenferie Toorak ROAD"));
    }


    @org.junit.Test
    public void Reading_Street_Test() {
        Assert.assertEquals("36 READING", encode("  36   READING "));

        Assert.assertEquals("36 Reading", encode("36 Reading street"));
    }


    private String encode(String address) {
        return new addressnoiseremoval().encode(address);
    }
}
