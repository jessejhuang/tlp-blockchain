/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
//with thanks from https://medium.com/digital-alchemy-holdings/learn-build-a-javascript-blockchain-part-1-ca61c285821e
package javablockchain;

import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.Random;

/**
 *
 * @author brad
 */
public class Blockchain {
    
    private static ArrayList<Block> chain = new ArrayList<Block>(); 
    //private static Block chain; //a chain of blocks...is...(wait for it)...a BLOCKCHAIN!!!!
    
    public Blockchain(int data){
        this.chain.add(createGenesis(data));
    }
    
    private Block createGenesis(int data){
        //Genesis block is first block, unique! We will generate some data for it here
        Timestamp currentTimeStamp = new Timestamp(System.currentTimeMillis());
        Block genesisBlock = new Block(currentTimeStamp, data);
        return genesisBlock;
    }
    
    private Block latestBlock(){
        return this.chain.get(this.chain.size()-1); //using ArrayList.get()
    }
    
    protected void addBlock(int data){
        //setup
        Timestamp currentTimeStamp = new Timestamp(System.currentTimeMillis());
        
        Block newBlock = new Block(currentTimeStamp, data);
      
        newBlock.setPreviousHash(this.latestBlock().getHash());
        newBlock.setHash(newBlock.calculateHash()); //not sure calc Hash should be public...
        this.chain.add(newBlock);
    }
    
    protected boolean validate(){
        int i =0;
        
        for(i=1; i < this.chain.size(); i++){ //start on 2nd block
            final Block currentBlock = this.chain.get(i);
            final Block previousBlock = this.chain.get(i-1);
          ///      System.out.println("before checking: ");
         //       System.out.println(currentBlock.getHash());
       //         System.out.println(currentBlock.calculateHash());
       //         System.out.println(); 
                
           
            if(!(currentBlock.getHash().equals(currentBlock.calculateHash()))){
                System.out.println("FAILED AT " + i + " 1st loop");
                System.out.println(currentBlock.getHash());
                System.out.println(currentBlock.calculateHash());
                return false;
            }
            
            if(!(currentBlock.getPreviousHash().equals(previousBlock.getHash()))){
                System.out.println("FAILED AT " + i + " 2nd loop");
                System.out.println(previousBlock.getHash());
                System.out.println(previousBlock.calculateHash());
                return false;
            }
        }
       
        return true;  //if blockchain's integrity is secure 
    }
    
    public void print(){
        int i=0;

        String upperBorder = "";
        String lowerBorder = "";
        String bigCurrentHashString="";
        String bigPreviousHashString="";
        
        System.out.println("size of chain is " +  this.chain.size());
        
        for(i=0; i < this.chain.size(); i++){
            if (i==0){//if genesis, format differently
                 upperBorder +=           "----------------------------------------------------------------------------   ";
                 bigCurrentHashString += "| BLOCK " + i + ":" + this.chain.get(i).getHash() + " | ->";/////////////////
                 bigPreviousHashString += "| LAST 0:                                                                  | ->";
                 lowerBorder +=           "----------------------------------------------------------------------------   ";
            }
            else{
                 upperBorder +=           "----------------------------------------------------------------------------   ";
                 bigCurrentHashString += "| BLOCK " + i + ":" + this.chain.get(i).getHash() + " | -> ";
                 bigPreviousHashString += "| LAST  " + i + ":" + this.chain.get(i).getPreviousHash() + " | -> ";
                 lowerBorder +=           "----------------------------------------------------------------------------   ";
            }
            
        }
        System.out.println(upperBorder);
        System.out.println(bigCurrentHashString);
        System.out.println(bigPreviousHashString);
        System.out.println(lowerBorder);
    }
    
}
