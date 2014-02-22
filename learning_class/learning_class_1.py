import sys

class pet:
        number_of_legs = 0
        name_of_pet =''
        character =''
        def amount_of_legs(self,character):
                print self.character
                return 'name of pet - %s, number of legs - %s' %(self.name_of_pet,self.number_of_legs)

def print_legs(objects,legs):
        for object,leg in zip(objects,legs):
                pet_name = object
                object = pet()
                object.number_of_legs = leg
                object.name_of_pet = pet_name
                object.character = 'nice'
                print object.amount_of_legs(object.character)

def main():
        arguments = sys.argv[1:]
        objects_list =[]
        legs_list =[]
        objects_list_boolean = 'true'
        for argument in arguments:
                if objects_list_boolean =='true':
                        objects_list.append(argument)
                        objects_list_boolean ='false'
                elif objects_list_boolean == 'false':
                        legs_list.append(argument)
                        objects_list_boolean = 'true'
        print_legs(objects_list,legs_list)


if __name__=="__main__":
        main()
