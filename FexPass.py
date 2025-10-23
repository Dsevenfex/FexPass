from utils.F import Logo,Line,clear_console
from colorama import Fore
from utils.password_generator import password_generate
import re



def Main():
     clear_console()
     Logo()
     Line()
     print(f" {Fore.GREEN}[1] Pwd Generator")
     print(f" {Fore.RED}[0] Exit")
     Line()
     number = input(f"{Fore.GREEN}Choose: ")
     if number == "1":
          clear_console()
          Logo()
          Line()
          print("If you don't have it, just write (N)")
          while True :
             Birth=input(f"{Fore.GREEN}Date of birth (dd/mm/yyyy): ")
             if Birth != "N":
              if re.match(r'^\d{2}/\d{2}/\d{4}$', Birth):
               break  
              else:
               print("(dd/mm/yyyy)")
             else:
              break
             
          while True :
             min_length=input("minimum pasword length :")
             try:
                main_min_length=int(min_length)
                if type(main_min_length) == int:
                  break  
                else:
                  print("(only number)")
             except:
                print("(only number)")
                

             

          user_data={
          "Username": input(f"{Fore.GREEN}Username: "),
          "Name":input(f"{Fore.GREEN}Name: "),
          "Surname":input(f"{Fore.GREEN}Surname: "),
          "Pet":input(f"{Fore.GREEN}Pet name: "),
          "Color":input(f"{Fore.GREEN}Favorite color: "),
          "Fnumber":input(f"{Fore.GREEN}Favorite number: "),
          "Fperson":input(f"{Fore.GREEN}Favorite person name: "),
          "Game":input(f"{Fore.GREEN}Favorite game: "),
          "Sport":input(f"{Fore.GREEN}Favorite sport: "),
          "Friend":input(f"{Fore.GREEN}Favorite friend: "),
          "Word":input(f"{Fore.GREEN}Favorite word: "),
          "Animal":input(f"{Fore.GREEN}Favorite animal: "),
          "Place":input(f"{Fore.GREEN}Favorite place: "),
          "Birth":Birth,
          "min_length":main_min_length
          }
          password_generate(user_data) # დასამატებელია
         
          clear_console()
          Logo()
          Line()     
     else:
          clear_console()
          Logo()
          Line()
          print(f"{Fore.RED}Invalid character!")
          input(f"{Fore.RED}Return Press enter: ")
          Line()

          Main()
  




if __name__ == "__main__":
     Main()