import math


def velocity(displacement, time):
    """
        Calculate velocity given displacement and time
        Parameters
        ----------
        displacement : float
        time: float

        Returns
        -------
        float
    """
    pass


def displacement(velocity, time, acceleration):
    """
        Calculate displacement given velocity and time
        Parameters
        ----------
        velocity : float
        time: float

        Returns
        -------
        float
    """
    pass


def average_velocity(velocity_list):
    """
        Calculate the average velocity given multiple velocities
        Parameters
        ----------
        velocity_list : list

        Returns
        -------
        float
    """
    pass


def acceleration(velocity, time):
    """
        Calculate the acceleration given velocity and time
        Parameters
        ----------
        velocity : float
        time: float

        Returns
        -------
        float
    """
    pass

def initial_velocity(final_velocity, acceleration, time):
    """
        Calculates the initial_velocity when given final_velocity, acceleration and time

        Parameters
        ----------
        final_velocity : float
        acceleration : float
        time : float

        Returns
        -------
        float
    """
    return final_velocity - acceleration * time


def final_velocity(initial_velocity, acceleration, time):
    """
        Calculates the final_velocity when given initial_velocity, acceleration and time

        Parameters
        ----------
        initial_velocity : float
        acceleration : float
        time : float

        Returns
        -------
        float
    """
    return initial_velocity + acceleration * time


def momentum(mass, velocity):
    """
        Calculates the momentum when given mass and velocity

        Parameters
        ----------
        mass : float
        velocity : float

        Returns
        -------
        float
    """
    return mass * velocity


def force(mass, acceleration):
    """
        Calculates the momentum when given mass and acceleration

        Parameters
        ----------
        mass : float
        acceleration : float

        Returns
        -------
        float
    """
    return mass * acceleration


def gravitational_force(M, m, r, G = 6.674 * ( 10 ** - 11 ) ) :
    """
        Calculates the gravitational_force when given Mass of object1 = M, Mass of object2 = m, Distance
        between center of masses = r and Gravitational constant = G

        Parameters
        ----------
        M : float
        m : float
        r : float

        Returns
        -------
        float
    """
    return  G * M * m  / r ** 2

def work(force, displacement, theta):
    """
       Calculates the work done by 
       the force while displacing
       an object at an angle theta
       
       Parameters
       ----------
       force : float
       displcement : float 
       theta : float
       
       Returns
       -------
       float
    """
    return force * displacement * math.cos(theta)

def power(work, time):
    """
       Power is the rate at which the work is done.
       Calculates the amountof work done divided by 
       the time it takes to do the work
       
       Parameters
       ----------
       work : float
       time : float
       
       Returns
       -------
       float
    """
    return work / time


def kinetic_energy(mass, velocity):
    """
       Calculates the energy associated 
       with an object with mass moving
       at a given velocity 
       
       Parameters
       ----------
       mass : float
       velocity : float
       
       Returns
       -------
       float
    """
    return (1/2) * mass * velocity**2


def total_energy(T, V):
    """
       Total energy of an object is 
       the sum of its kinetic energy 
       'T' and potential energy 'V'
       
       Parameters
       ----------
       T : float
       V : float
       
       Returns
       -------
       float
    """
    return T + V


def angular_displacement(l, r):
    """
       Calculates the angular displacement of
       an object whose linear displacement is 
       'l' and radius of the path traced is 'r'
       
       Parameters
       ----------
       l : float
       r : float
       
       Returns
       -------
       float
    """
    return l / r


def angular_velocity(v, r):
    """
       Calculates the angular velocity of an
       object whose linear velocity is 'v'
       and radius of the path traced is 'r'
       
       Parameters
       ----------
       v : float
       r : float
       
       Returns
       -------
       float
    """
    return v / r


def angular_acceleration(a, r):
    """
       Calculates the angular acceleration of an
       object whose linear acceelration is 'a' and 
       radius of the path traced by the object is 'r'
      
       Parameters
       ----------
       a : float
       r : float
       
       Returns
       -------
       float
    """
    return a / r


def moment_of_inertia(m, k):
    """
       Calculates the moment of inertia of an object
       of mass 'm' with radius of gyration 'k'
      
       Parameters
       ----------
       m : float
       k : float
       
       Returns
       -------
       float
    """
    return m * k**2


def angular_momentum(m, v, r, theta):
    """
       Calculates the angular momentum of an object 
       of mass 'm' whose linear velocity is 'v' and 
       radius of the path traced by the object is 'r',
       angle between velocity and radius is 'theta'
      
       Parameters
       ----------
       m : float
       v : float
       r : float
       theta : float
       
       Returns
       -------
       float
    """
    return m * v * r * math.sin(theta) 


def centripetal_acceleration(v, r):
    """
       Calculates the centripetal acceleration of
       an object whose linear velocity is 'v' and 
       radius of the path traced by the object is 'r'
      
       Parameters
       ----------
       v : float
       r : float
       
       Returns
       -------
       float
    """
    return v**2 / r


def centripetal_force(m, v, r):
    """
       Centripetal force is the net force
       that acts on an object with mass 'm' to 
       keep it moving with a velocity 'v' tracing
       a circular path of radius 'r'
       
       Parameters
       ----------
       m : float
       v : float 
       r : float
       
       Returns
       -------
       float
    """
    return m * v**2 / r


def angular_kinetic_energy(i, w):
    """
       Calculates the angular kinetic energy
       of an object with moment of inertia 'I'
       and angular velocity 'w'
       
       Parameters
       ----------
       i : float
       w: float 
       
       Returns
       -------
       float
    """
    return (1/2) * i * w**2


def torque(r, f, theta):
    """
       Calculates the torque acting on an object
       where 'r' is the radius, 'f' is the force
       and 'theta' is the angle between 'r' and 'f'
      
       Parameters
       ----------
       r : float
       f : float
       theta : float
       
       Returns
       -------
       float
    """
    return r * f * math.sin(theta)


def friction():
    pass


def normal_force():
    pass


