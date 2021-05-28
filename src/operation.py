
# ==================================================================================================

class Operation:

    # ----------------------------------------------------------------------------------------------

    def __init__(self, name, args, res, pred=None, zflag=None):
        """
        Constructor.

        :param name: name of operation
        :param args: list of arguments
        :param res: operation result
        :param pred: predicate under with operation is set
        :param zflag: zero flag for result register
        """

        self.Name = name

        if name == 'add-f':
            self.check_operation(name, args, res, pred, zflag,
                                 args_count=2, args_types=['f', 'f'],
                                 res_type='f', allow_zflag=True)
            pass
        else:
            raise Exception('Unknown operation name.')

        self.Args = args
        self.Res = res
        self.Pred = pred
        self.ZFlag = zflag

    # ----------------------------------------------------------------------------------------------

    def check_operation(self, name, args, res, pred, zflag,
                        args_count, args_types, res_type, allow_zflag):
        """
        Check operation.

        :param name: name of operation
        :param args: list of arguments
        :param res: result of the operation
        :param pred: predicate
        :param zflag: zero flag
        :param args_count: count of arguments
        :param args_types: arguments types
        :param res_type: result type
        :param allow_zflag: allow zero flag or not
        """

        if len(args) != args_count:
            raise Exception('Wrong arguments count in {0} operation.'.format(name))

        for i in range(args_count):
            if args[i].T != args_types[i]:
                raise Exception('Wrong argument type in {0} operation.'.format(name))

        if res.T != res_type:
            raise Exception('Wrong result type in {0} operation.'.format(name))

        if not allow_zflag:
            if zflag is not None:
                raise Exception('No zflag is allowed for {0} operation.'.format(name))

        w = args[0].N
        for i in range(len(args)):
            if args[i].N != w:
                raise Exception('Wrong arguments width in {0} operation.'.format(name))
        if res.N != w:
            raise Exception('Wrong result width in {0} operation.'.format(name))
        if pred is not None:
            if pred.N != w:
                raise Exception('Wrong predicate width i {0} operation.'.format(name))

    # ----------------------------------------------------------------------------------------------

    def zflag_str(self):
        """
        Get zero flag string for print.

        :return: zero flag string
        """

        z = ''
        if self.ZFlag:
            z = '[z]'

        return z

    # ----------------------------------------------------------------------------------------------

    def print_s(self):
        """
        Print short version of operation (without values).
        """

        # Form arguments string.
        args_str = ', '.join([a.str_s() for a in self.Args])

        # Form predicate string.
        pred_str = ''
        if self.Pred is not None:
            pred_str = ' ? {0}'.format(self.Pred.str_s())

        # Form res string.
        res_str = self.Res.str_s()

        # Print.
        print('{0}{1} : {2}{3} -> {4}'.format(self.Name, self.zflag_str(),
                                              args_str, pred_str, res_str))

    # ----------------------------------------------------------------------------------------------

    def print_l(self):
        """
        Print operation data.
        """

        # Print head of operation.
        print('{0}{1}'.format(self.Name, self.zflag_str()))

        # Print args.
        for i in range(len(self.Args)):
            print('    a | {0}'.format(self.Args[i].str_l()))

        # Print predicate.
        if self.Pred is not None:
            print('    p | {0}'.format(self.Pred.str_l()))

        # Print result.
        print('    r | {0}'.format(self.Res.str_l()))

# ==================================================================================================