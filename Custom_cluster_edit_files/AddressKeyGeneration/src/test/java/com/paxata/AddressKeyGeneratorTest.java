package com.paxata;

import org.junit.Assert;

/**
 * Created by callumfinlayson on 8/20/20.
 */
public class AddressKeyGeneratorTest {

    /**
     * Unit test for simple App.
     */
        @org.junit.Test
        public void Bill_nicknameFor_William() {
            Assert.assertEquals("MNSM0NK,SM0NKMN", encode("1 Main Something st"));
            Assert.assertEquals("MNBR0R,BR0RMN", encode("1 Main brother st"));
        }

        @org.junit.Test
        public void Bob_Rob_Bobby_and_Robert() {
            Assert.assertEquals("BWTLTR,WTLTRB", encode("Unit 15 , 32B Wattletree Road"));
            Assert.assertEquals("TRKKLNF,WTLTRKL,WTLTRTR", encode("WATTLETREE Toorak Glenferie ROAD  "));
            Assert.assertEquals("KLNFRTR,WTLTRTR,WTLTRKL", encode("WATTLETREE Glenferie Toorak ROAD"));
        }

        @org.junit.Test
        public void Longer_names() {
            Assert.assertEquals("RBRTSM0,SM0RBRT", encode("Bob Smith"));
        }


        @org.junit.Test
        public void Reading_Street_Test() {
            Assert.assertEquals("RTNK", encode("  36   READING "));

            Assert.assertEquals("RTNK", encode("36 Reading street"));
        }


        private String encode(String name) {
            return new AddressKeyGenerator().encode(name);
        }
    }
