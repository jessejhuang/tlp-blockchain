/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package javablockchain;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.sql.Timestamp;
import java.util.Random;

/**
 *
 * @author brad
 */
public class JavaBlockchain {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws NoSuchAlgorithmException {
      
        Blockchain blockchain = new Blockchain(getRandomData());
        blockchain.addBlock(getRandomData());
        blockchain.addBlock(getRandomData());
        blockchain.addBlock(getRandomData());
        blockchain.addBlock(getRandomData());
        blockchain.print();
        if(blockchain.validate() == true){
            System.out.println("All good! Keep on minin'!");
        }
        else{
            System.out.println("ERROR: BLOCKCHAIN IS CORRUPTED");
        }
    }
    
    private Timestamp getCurrentTimestamp(){
        Timestamp currentTimeStamp = new Timestamp(System.currentTimeMillis());
        return currentTimeStamp;
    }
    private static int getRandomData(){
        Random random = new Random();
        int randomData = random.nextInt(100000) + 1;
        return randomData;
    }
    
//NOTE: the whole point of SHA-512 is that it is in-fact REVERSIBLE!
//This is a tamper detection mechanism/THE tamper detection mechanism!
//Since every block holds the previous hash, you would have to somehow
//bust into every block to tamper it
//thus, the power of Blockchain is the power of SHA-512
//, which is a nearly unreversible hashing algorithm!
// even more brilliantly, you use the previous hash to 
    

}
