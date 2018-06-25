/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
//SHA-256 from baeldung http://www.baeldung.com/sha-256-hashing-java
//Basic blockchain algorithm from https://medium.com/digital-alchemy-holdings/learn-build-a-javascript-blockchain-part-1-ca61c285821e

package javablockchain;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.sql.Timestamp;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author brad
 */
public class Block {
    
    private int index = 0;
    private Timestamp timestamp;
    private int data; //obvi a simplification..
    private String previousHash = "0";
    private String hash= "";
    private int nonce = 0;
    
    public Block(Timestamp timestamp, int data){
        this.timestamp = timestamp;
        this.data = data;
        this.hash = this.calculateHash();
    }
    
    private static String bytesToHex(byte[] hash){
    StringBuffer hexString = new StringBuffer();
    for (int i=0; i<hash.length; i++){
    String hex = Integer.toHexString(0xff & hash[i]);
    if(hex.length() == 1) hexString.append('0');
        hexString.append(hex);
    }
    return hexString.toString();
}
    
    public String calculateHash(){ 
        
        String stringToBeHashed = this.index + this.previousHash + this.timestamp + this.data + this.nonce;
        
        MessageDigest digest;
        try {
            digest = MessageDigest.getInstance("SHA-256");
            byte[] encodedhash = digest.digest(stringToBeHashed.getBytes(StandardCharsets.UTF_8));
            String sha256hash = bytesToHex(encodedhash);
          //  System.out.println(sha256hash);
            return (sha256hash);
        }
         catch (NoSuchAlgorithmException ex) {
            Logger.getLogger(Block.class.getName()).log(Level.SEVERE, null, ex);
        }
        return "-1";
    }
    public Timestamp getTimestamp(){
        return this.timestamp;
    }
    public int getData(){
        return this.data;
    }
    public String getPreviousHash(){
        return this.previousHash;
    }
    public void setPreviousHash(String previousHash){
        this.previousHash = previousHash;
    }
    public String getHash(){
        return this.hash;
    }
    public void setHash(String hash){
        this.hash = hash;
    }
    public int getNonce(){
        return this.nonce;
    }

}
