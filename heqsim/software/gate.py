
class QuantumGate:
    """Software interface of a quantum gate"""

    def __init__(self, name, index, target_index=None, theta=None):
        """Detail of a quantum gate

        Args:
            name (str): The name of this quantum gate
            index (int): The qubit index that this gate is applied to
            target_index (int, optional): The index of target qubit of a controlled quantum gate. Defaults to None.
            theta (float, optional): The rotation angle of a rotation quatum gate. Defaults to None.
        """
        self.name = name
        self.index = index
        self.target_index = target_index
        self.theta = theta
        self.remote_cnot_id = None
        self.link_id = None
        self.role = None

    def set_remote_cnot_id(self, remote_cnot_id):
        """Add a remote CNOT id to this remote CNOT gate

        Args:
            remote_cnot_id (int): A new remote CNOT gate id
        """
        self.remote_cnot_id = remote_cnot_id

    def set_link_id(self, link_id):
        """Add link id to this remote CNOT gate (specify the link where this remote CNOT gate is going to communicate)

        Args:
            link_id (int): A new link id
        """
        self.link_id = link_id

    def set_role(self, role):
        """Add role to this remote CNOT gate

        Args:
            role (str): "control" or "target"
        """
        self.role = role
