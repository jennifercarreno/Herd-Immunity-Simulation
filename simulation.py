import random, sys
# from typing_extensions import final
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    ''' Main class that will run the herd immunity simulation program.
    Expects initialization parameters passed as command line arguments when file is run.

    Simulates the spread of a virus through a given population.  The percentage of the
    population that are vaccinated, the size of the population, and the amount of initially
    infected people in a population are all variables that can be set when the program is run.
    '''

    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        ''' Logger object logger records all events during the simulation.
        Population represents all Persons in the population.
        The next_person_id is the next available id for all created Persons,
        and should have a unique _id value.
        The vaccination percentage represents the total percentage of population
        vaccinated at the start of the simulation.
        You will need to keep track of the number of people currently infected with the disease.
        The total infected people is the running total that have been infected since the
        simulation began, including the currently infected people who died.
        You will also need to keep track of the number of people that have die as a result
        of the infection.

        All arguments will be passed as command-line arguments when the file is run.
        HINT: Look in the if __name__ == "__main__" function at the bottom.
        '''
        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding parts of the simulation. 

        # TODO: Call self._create_population() and pass in the correct parameters.
        # Store the array that this method will return in the self.population attribute.
        
        # TODO: Store each newly infected person's ID in newly_infected attribute.
        # At the end of each time step, call self._infect_newly_infected()
        # and then reset .newly_infected back to an empty list.

        

        self.population = [] # List of Person objects
        self.infected_people = []
        self.pop_size = pop_size # Int

        self.next_person_id = 0 # Int
        self.virus = virus # Virus object

        self.initial_infected = initial_infected # Int
        self.total_infected = 0 # Int
        self.current_infected = 0 # Int

        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.vaccinated_saved = 0
        self.total_dead = 0 # Int
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(self.virus.name, pop_size, vacc_percentage, initial_infected)
        self.logger = Logger(self.file_name)
        self.newly_infected = []
        self._create_population(initial_infected)
        self.logger.write_metadata(self.pop_size, self.vacc_percentage, self.virus.name, self.virus.mortality_rate, self.virus.repro_rate)


    def _create_population(self, initial_infected):
        '''This method will create the initial population.
            Args:
                initial_infected (int): The number of infected people that the simulation
                will begin with.

            Returns:
                list: A list of Person objects.

        '''
        # TODO: Finish this method!  This method should be called when the simulation
        # begins, to create the population that will be used. This method should return
        # an array filled with Person objects that matches the specifications of the
        # simulation (correct number of people in the population, correct percentage of
        # people vaccinated, correct number of initially infected people).

        # Use the attributes created in the init method to create a population that has
        # the correct intial vaccination percentage and initial infected.

        pop_size = int(self.pop_size)
        
        for i in range(pop_size):
            person = Person(i,False)
            self.population.append(person)
        
        for i in range(initial_infected):
            infected_person = random.choice(self.population)
            infected_person.is_infected = True
            self.infected_people.append(infected_person)


    def _simulation_should_continue(self):
        ''' The simulation should only end if the entire population is dead
        or everyone is vaccinated.

            Returns:
                bool: True for simulation should continue, False if it should end.
        '''
        # TODO: Complete this helper method.  Returns a Boolean.

        total_vaccinated = 0

        for person in self.population:
            if person.is_vaccinated:
                total_vaccinated += 1
        
        print(self.pop_size)
        print(self.total_dead)
        # print(self.infected_people)
        print(total_vaccinated)
        print(self.vaccinated_saved)
        

        if total_vaccinated == self.pop_size or self.total_dead == self.pop_size or len(self.infected_people) == 0:
            return False
        else: 
            return True

    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        # TODO: Finish this method.  To simplify the logic here, use the helper method
        # _simulation_should_continue() to tell us whether or not we should continue
        # the simulation and run at least 1 more time_step.

        # TODO: Keep track of the number of time steps that have passed.
        # HINT: You may want to call the logger's log_time_step() method at the end of each time step.
        # TODO: Set this variable using a helper
        time_step_counter = 0
        # should_continue = None

        while self._simulation_should_continue():
            # TODO: for every iteration of this loop, call self.time_step() to compute another
            # round of this simulation.
            time_step_counter += 1
            self.time_step()
            print(f"we are on this step: {time_step_counter}")
            print(f"infected people: {len(self.infected_people)}")

            
        print(f'The simulation has ended after {time_step_counter} turns.')

    def time_step(self):
        ''' This method should contain all the logic for computing one time step
        in the simulation.

        This includes:
            1. 100 total interactions with a random person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''
        # TODO: Finish this method.

        interaction_counter = 0 

        for person1 in self.infected_people:
            for i in range(100):
                person2 = random.choice(self.population)
                if person1.is_alive and person2.is_alive:
                    self.interaction(person1, person2)
                    interaction_counter += 1
            
            if person1.did_survive_infection(self.virus):
                
                self.logger.log_infection_survival(person1, survived = False)
                self.infected_people.remove(person1)
                # print("did survive returned false, person did not die")
            else:
                self.logger.log_infection_survival(person1, survived = True)
                self.infected_people.remove(person1)
                # print("someone died")
                self.total_dead +=1  
        
        self._infect_newly_infected()

        
        




    def interaction(self, person1, person2):
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.

        Args:
            person1 (person): The initial infected person
            person2 (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed
        # in as params
        assert person1.is_alive == True
        assert person2.is_alive == True

        # TODO: Finish this method.
        #  The possible cases you'll need to cover are listed below:
            # random_person is vaccinated:
            #     nothing happens to random person.
            # random_person is already infected:
            #     nothing happens to random person.
            # random_person is healthy, but unvaccinated:
            #     generate a random number between 0 and 1.  If that number is smaller
            #     than repro_rate, random_person's ID should be appended to
            #     Simulation object's newly_infected array, so that their .infected
            #     attribute can be changed to True at the end of the time step.
        
        
        if person2.is_vaccinated:
            # print("person is vaccinated")
            self.logger.log_interaction(person1, person2, person2_vacc=True)
            self.vaccinated_saved += 1
        elif person2.is_infected:
            # print("person is infected, nothing happens")
            self.logger.log_interaction(person1, person2, person2_sick = True)
        elif person2.is_vaccinated is False and person2.is_infected is False:
            random_number = random.random()
            if random_number < self.virus.repro_rate:
                if person2 not in self.newly_infected:
                    self.newly_infected.append(person2) 
                    self.logger.log_interaction(person1, person2, person2_sick=person2.is_infected, person2_vacc=person2.is_vaccinated)

        
        # TODO: Calls logger method during this method.
        
         

    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.

        for person in self.newly_infected:
            person.is_infected = True
            self.infected_people.append(person)

        self.newly_infected = []
        




if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name = str(params[0])
    repro_rate = float(params[1])
    mortality_rate = float(params[2])

    pop_size = int(params[3])
    vacc_percentage = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_rate, mortality_rate)
    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)

    sim.run()
