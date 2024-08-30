package com.paxata.custom.clustering;
import org.junit.Test;
import org.junit.Assert;

public class nicknameTest {
    @Test
    public void Bill_nicknameFor_William() {
        Assert.assertEquals("WLM", encode("Bill"));
    }

    @Test
    public void Bob_Rob_Bobby_and_Robert() {
        Assert.assertEquals(encode("Robert"), encode("Bob"));
        Assert.assertEquals(encode("Robert"), encode("Rob"));
        Assert.assertEquals(encode("Robert"), encode("Bobby"));
    }

    @Test
    public void Victor_noNickname() {
        Assert.assertEquals("FKTR", encode("Victor"));
    }

    private String encode(String name) {
        return new nickname().encode(name);
    }
}