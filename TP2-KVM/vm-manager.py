import libvirt
import sys
import os

def hyper_info():
   print("Informations sur la machine Hypervisor")
   print("\nHostname:: "+conn.getHostname())
   print("Hypervisor type:: "+conn.getType())
   print("Connected on:: "+conn.getURI())
   print("\nCPU Model:: "+str(conn.getInfo()[0]))
   print("Memory Size:: "+str(conn.getInfo()[1]))
   #print("Memoire disponible:: "+str(conn.getFreeMemory()))

def list_vm():
   try:
     print("Les machines virtuelles existantes dans " + conn.getHostname() +":\n")
     domains = conn.listAllDomains()
     for i in range(len(domains)):
       dom = domains[i]
       print(str(i)+': '+dom.name())
       print("   Etat = "+str(dom.info()[0]))
       print("   Max Memoire = "+str(dom.info()[1]))
       print("   Nombre de CPUsvirt = "+str(dom.info()[3]))
       print("   Temps CPU (en ns) = "+str(dom.info()[2])) 
       print("   isActive = "+str(dom.isActive()))
   except libvirt.libvirtError:
     print("Failed to list existing domains")  

def start_vm():
    print("""
Menu des Machines Virtuelles
 veuillez choisir une machine a demarrer
   """)
    domains = conn.listAllDomains()
    for i in range(len(domains)):
       dom = domains[i]
       print(str(i)+': '+dom.name())
       print("   isActive = "+str(dom.isActive()))
    choice = int(raw_input("\nVotre choix:: "))
    while(not (choice in range(len(domains)))):
      print(str(choice) +" n'est pas un choix valide")
      choice = int(raw_input("\nVotre choix:: "))
    try:
       if choice in range(len(domains)):
         if domains[choice].isActive():
            print("Machine is already active")
         else:
            domains[choice].create()
            print("Machine activated successfully")
            os.system("virt-viewer "+domains[choice].name()+"&");
    except: 
       print("err starting vm") 

def shutdown_vm():
    print("""
Menu des Machines Virtuelles
 veuillez choisir une machine a arreter
   """)
    domains = conn.listAllDomains()
    for i in range(len(domains)):
       dom = domains[i]
       print(str(i)+': '+dom.name())
       print("   isActive = "+str(dom.isActive()))
    choice = int(raw_input("\nVotre choix:: "))
    while(not (choice in range(len(domains)) ) ):
      print(str(choice) +" n'est pas un choix valide")
      choice = int(raw_input("\nVotre choix:: "))
    try:
       if choice in range(len(domains)):
         if not domains[choice].isActive():
            print("Machine is already shutdown")
         else:
            domains[choice].destroy()
            print("Machine is being shutdown")
    except: 
       print("err shuting down vm") 

def ip_addr_vm():
    print("""
Menu des Machines Virtuelles
 veuillez choisir une machine 
   """)
    domains = conn.listAllDomains()
    for i in range(len(domains)):
       dom = domains[i]
       print(str(i)+': '+dom.name())
       print("   isActive = "+str(dom.isActive()))
    choice = int(raw_input("\nVotre choix:: "))
    while(not (choice in range(len(domains)) ) ):
      print(str(choice) +" n'est pas un choix valide")
      choice = int(raw_input("\nVotre choix:: "))
    try:
       if choice in range(len(domains)):
         if not domains[choice].isActive():
            print("Machine is not active")
         else:
            ifaces = domains[choice].interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
            for (name, val) in ifaces.iteritems():
                if val['addrs']:
                   for ipaddr in val['addrs']:
                       if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4: print("IP addresse : "+ ipaddr['addr'])
            
    except: 
       print("err getting ip of vm")

def clear():
   if os.name=='posix':
     os.system("clear")
   elif os.name=='nt':
     os.system("cls")

def display_menu():
   print("""
==========================================================
Programme de gestion des machines virtuelles
 veuillez entrer votre choix

0) Nom de la machine hyperviseur
1) Lister les machines virtuelles
2) Demarrer une machine 
3) Arreter une machine
4) L'adresse IP d'une machine virtuelles

5:: Quitter le programme
   """)

try:
  conn = libvirt.open("qemu:///system")
except libvirt.libvirtError:
  print("Failed to open connection to the hypervisor")
  sys.exit(1)


while(True):
  
  clear()
  display_menu()  
  choix = int(raw_input("Votre choix:: "))
  clear()
  print("==========================================================")

  if choix==0:
    hyper_info()
    pass
  elif choix==1:
    list_vm()
    pass
  elif choix==2:
    start_vm()
    pass
  elif choix==3:
    shutdown_vm()
    pass
  elif choix==4:
    ip_addr_vm()
    pass
  elif choix==5:
    clear()
    conn.close()
    sys.exit(0)
  else:
    print(str(choix) +" n'est pas un choix valide")
  raw_input("\nPress any key to continue ...")