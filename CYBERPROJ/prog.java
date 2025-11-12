import java.util.*;
import java.net.*;

public class main{
    public static void main(String[] args){
        try{
            InetAddress address = InetAddress.getLocalHost();
	System.out.println("Name of the Computer: " + address.getHostName());
            System.out.println("IP Address is: " + address.getHostAddress());
        }
        catch(UnknownHostException e){
            System.out.println("Could not find System address");
        }
    }
}
