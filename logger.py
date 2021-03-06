class Logger(object):
    def __init__(self, file_name):
        # TODO:  Finish this initialization method. The file_name passed should be the
        # full file name of the file that the logs will be written to.
        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num):
        # TODO: Finish this method. This line of metadata should be tab-delimited
        # it should create the text file that we will store all logs in.
        # TIP: Use 'w' mode when you open the file. For all other methods, use
        # the 'a' mode to append a new log to the end, since 'w' overwrites the file.
        # NOTE: Make sure to end every line with a '/n' character to ensure that each
        # event logged ends up on a separate line!

        log_file = open(self.file_name, "w")
        log_file.write(f"Population size: {pop_size}, Percent Vaccinated: {vacc_percentage}, Virus Name: {virus_name}, Mortality Rate: {mortality_rate}, Reproduction Rate: {basic_repro_num} \n")
        log_file.close()

    def log_interaction(self, person1, person2, person2_sick=None,
                        person2_vacc=None, did_infect=None):
        '''
        The Simulation object should use this method to log every interaction
        a sick person has during each time step.

        The format of the log should be: "{person.ID} infects {random_person.ID} \n"

        or the other edge cases:
            "{person.ID} didn't infect {random_person.ID} because {'vaccinated' or 'already sick'} \n"
        '''
        # TODO: Finish this method. Think about how the booleans passed (or not passed)
        # represent all the possible edge cases. Use the values passed along with each person,
        # along with whether they are sick or vaccinated when they interact to determine
        # exactly what happened in the interaction and create a String, and write to your logfile.
        
        log_file = open(self.file_name, "a")
        if person2_vacc is False or person2_sick is False:
            log_file.write(f"{person1._id} infects {person2._id}\n")
        elif person2_vacc: 
            log_file.write(f"{person1._id} didn't infect {person2._id} because vaccinated \n")
        elif person2_sick:
            log_file.write(f"{person1._id} didn't infect {person2._id} because they were already sick \n")

        log_file.close()

    def log_infection_survival(self, person, survived = None):
        ''' The Simulation object uses this method to log the results of every
        call of a Person object's .resolve_infection() method.

        The format of the log should be:
            "{person.ID} died from infection\n" or "{person.ID} survived infection.\n"
        '''
        # TODO: Finish this method. If the person survives, did_die_from_infection
        # should be False.  Otherwise, did_die_from_infection should be True.
        # Append the results of the infection to the logfile
        log_file = open(self.file_name, "a")
        if survived:
            log_file.write(f"{person._id} survived infection \n")
        elif survived == False:
            log_file.write(f"{person._id} died from infection \n")

        log_file.close()
        

    def log_answers(self, percentage):
        log_file = open(self.file_name, "a")
        log_file.write(f"percentage of population infected before the virus burned out: {percentage}")
        log_file.close()

        pass
