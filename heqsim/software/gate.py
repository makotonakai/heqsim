
class QuantumGate:
    """Software interface of a quantum gate"""

    def __init__(self, name, index, target_index=None, theta=None):
        """Detail of a quantum gate

        Args:
            name (str): name of this quantum gate
            index (int): qubit index that this gate is applied to
            target_index (int, optional): index of target qubit of a controlled quantum gate. Defaults to None.
            theta (float, optional): rotation angle of a rotation quatum gate. Defaults to None.
        """
        self.name = name
        self.index = index
        self.target_index = target_index
        self.theta = theta

    def set_remote_cnot_id(self, remote_cnot_id):
        """Add a remote CNOT id to this remote CNOT gate

        Args:
            remote_cnot_id (int): new remote CNOT gate id
        """
        self.remote_cnot_id = remote_cnot_id

    def set_link_id(self, link_id):
        """Add link id to this remote CNOT gate (specify the link where this remote CNOT gate is going to communicate)

        Args:
            link_id (int): new link id
        """
        self.link_id = link_id

    def set_role(self, role):
        """Add role to this remote CNOT gate

        Args:
            role (str): "control" or "target"
        """
        self.role = role
