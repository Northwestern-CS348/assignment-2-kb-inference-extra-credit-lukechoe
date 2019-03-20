import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument
        Args:
            fact (Fact): Fact we're searching for
        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument
        Args:
            rule (Rule): Rule we're searching for
        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact|Rule) - the fact or rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB
        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB
        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)
        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

            # Make sure to write edge case that if the retracted fact
            # is supported by something -  exit?
    def kb_retract(self, fact_or_rule):
        """Retract a fact from the KB
        Args:
            fact (Fact) - Fact to be retracted
        Returns:
            None
        """



        printv("Retracting {!r}", 0, verbose, [fact_or_rule])
        ####################################################
        # Student code goes here


        if fact_or_rule in self.facts:
            ind = self.facts.index(fact_or_rule)
            f_r = self.facts[ind]
        elif fact_or_rule in self.rules:
            ind = self.rules.index(fact_or_rule)
            f_r = self.rules[ind]
        else:
            print("Fact/Rule not found???????")
            return


        if isinstance(f_r, Rule) and len(f_r.supported_by) == 0:
            return
        if len(f_r.supported_by) > 0:
            return


        for f in f_r.supports_facts:

            ind3 = f.supported_by.index(f_r)
            if ind3 % 2 == 1:
                tmp = f.supported_by[ind3-1]
                f.supported_by.remove(tmp)
                tmp = f.supported_by[ind3-1]
                f.supported_by.remove(tmp)
            elif ind3 % 2 == 0:
                tmp = f.supported_by[ind3]
                f.supported_by.remove(tmp)

                tmp = f.supported_by[ind3]
                f.supported_by.remove(tmp)

            if len(f.supported_by) == 0:
                ind3 = self.facts.index(f)
                temp = self.facts[ind3]
                #self.facts.remove(self.facts[ind3])
                self.kb_retract(temp)



        for r in f_r.supports_rules:
            ind3 = r.supported_by.index(f_r)
            #print('***************************************************', r.supported_by[ind3])
            if ind3 % 2 == 1:
                tmp = r.supported_by[ind3-1]
                r.supported_by.remove(tmp)
                tmp = r.supported_by[ind3-1]
                r.supported_by.remove(tmp)
            elif ind3 % 2 == 0:
                tmp = r.supported_by[ind3]
                r.supported_by.remove(tmp)

                tmp = r.supported_by[ind3]
                r.supported_by.remove(tmp)

            print('...')
            if (len(r.supported_by)) == 0:
                print('ooooooooooooooookkkkkkkkkkkkkkkkkkkay we got here')
                ind3 = self.rules.index(r)
                temp = self.rules[ind3]
                self.rules.remove(self.rules[ind3])
                self.kb_retract(temp)


        if isinstance(f_r, Fact) and len(f_r.supported_by) == 0:
            del self.facts[ind]

    result = ""

    def kb_explain(self, fact_or_rule):
        """
        Explain where the fact or rule comes from
        Args:
            fact_or_rule (Fact or Rule) - Fact or rule to be explained
        Returns:
            string explaining hierarchical support from other Facts and rules
        """
        ####################################################
        # Student code goes here


        if isinstance(fact_or_rule, Fact):
            if fact_or_rule in self.facts:
                self.result += "fact: " + (str(fact_or_rule.statement)) + '\n'
                ans = self._get_fact(fact_or_rule)
            else:
                return "Fact is not in the KB"
        if isinstance(fact_or_rule, Rule):
            if fact_or_rule in self.rules:
                self.result += "rule: ("
                for left in fact_or_rule.lhs:
                    self.result += str(left) + ", "
                ans = self._get_rule(fact_or_rule)
            else:
                return "Rule is not in the KB"
        # call helper
        self.helper(ans, 0)
        return self.result



        """
        f_r = self.find_in_kb(fact_or_rule)
        if f_r == False:
            if isinstance(fact_or_rule, Fact):
                return "Fact is not in the KB"
            elif isinstance(fact_or_rule, Rule):
                return "Rule is not in the KB"
            else:
                return False

        string_answer = ""
        if len(f_r.supported_by) == 0:
            if isinstance(f_r, Fact):
                string_answer += "fact: "
                string_answer += str(f_r.statement)
                string_answer += " ASSERTED"
            if isinstance(f_r, Rule):
                string_answer += "rule: ("
                if len(f_r.lhs) > 1:
                    incr = 0
                    for r in f_r.lhs:
                        string_answer += str(r)
                        if incr == len(f_r.lhs) -1:
                            break
                        string_answer += ', '
                        incr += 1
                else:
                    string_answer += str(f_r.lhs[0])

                string_answer += ") -> "
                string_answer += str(f_r.rhs)
                string_answer += ' ASSERTED\n'


        if len(f_r.supported_by) > 0:
            stack = []
            if isinstance(f_r, Fact):
                string_answer += "fact: "
                string_answer += str(f_r.statement)
                string_answer += '\n'
            if isinstance(f_r, Rule):
                string_answer += "rule: "
                for r in f_r.lhs:
                    string_answer += str(r)
                string_answer += " -> "
                string_answer += str(f_r.rhs)
                string_answer += '\n'

            spaces = "  "
            counter = -2
            for supports in f_r.supported_by:
                stack.append([supports, counter])
            stack = stack[::-1]

            while len(stack) > 0:
                tmp = stack.pop()

                #print(tmp[0][0])

                new_fr1 = self.find_in_kb(tmp[0][0])
                new_fr2 = self.find_in_kb(tmp[0][1])
                new_counter = tmp[1]
                new_counter += 4

                #string_answer += "                    "
                #string_answer += str(new_counter)
                s = self.make_str(new_counter)
                string_answer += s
                #string_answer += spaces
                string_answer += "SUPPORTED BY\n"

                if isinstance(new_fr1, Fact) and isinstance(new_fr2, Rule):
                    string_answer += s
                    string_answer += "  "
                    string_answer += "fact: "
                    string_answer += str(new_fr1.statement)
                    if self.is_asserted(new_fr1):
                        string_answer += " ASSERTED"
                    string_answer += '\n'
                    string_answer += s
                    string_answer += "  "
                    string_answer += "rule: ("
                    if len(new_fr2.lhs) > 1:
                        incr = 0
                        for r in new_fr2.lhs:
                            string_answer += str(r)
                            if incr == len(new_fr2.lhs) -1:
                                break
                            string_answer += ', '
                            incr += 1
                    else:
                        string_answer += str(new_fr2.lhs[0])

                    string_answer += ") -> "
                    string_answer += str(new_fr2.rhs)
                    if self.is_asserted(new_fr2):
                        string_answer += " ASSERTED"
                    string_answer += '\n'

                if isinstance(new_fr2, Fact) and isinstance(new_fr1, Rule):
                    string_answer += s
                    string_answer += "  "
                    string_answer += "fact: "
                    string_answer += str(new_fr2.statement)
                    if self.is_asserted(new_fr2):
                        string_answer += " ASSERTED"
                    string_answer += '\n'
                    string_answer += s
                    string_answer += "  "
                    string_answer += "rule: ("
                    if len(new_fr2.lhs) > 1:
                        incr = 0
                        for r in new_fr2.lhs:
                            string_answer += str(r)
                            if incr == len(new_fr2.lhs) -1:
                                break
                            string_answer += ', '
                            incr += 1
                    else:
                        string_answer += str(new_fr2.lhs[0])

                    string_answer += ") -> "
                    string_answer += str(new_fr1.rhs)
                    if self.is_asserted(new_fr1):
                        string_answer += " ASSERTED"
                    string_answer += '\n'
                #print('wwwwwwwwwww', type(new_fr))
                if new_fr1 != False and new_fr2 != False:

                    #for supports in new_fr1.supported_by:
                    #    stack.append([supports,new_counter])
                    #for i in range(len(new_fr1.supported_by), 0, -1):
                    #    print('--------------- this far' , i)
                    #    stack.append([new_fr1.supported_by[i], new_counter])
                    if len(new_fr1.supported_by) > 0:
                        for j in reversed(range(0, len(new_fr1.supported_by))):
                            stack.append([new_fr1.supported_by[j], new_counter])

                    #for supports in new_fr2.supported_by:
                    #    stack.append([supports,new_counter])
                    if len(new_fr2.supported_by) > 0:
                        for j in reversed(range(0, len(new_fr2.supported_by))):
                            stack.append([new_fr2.supported_by[j], new_counter])


        return string_answer
        """


    def helper(self, fact_or_rule, indents):
        if len(fact_or_rule.supported_by) > 0 and len(fact_or_rule.supported_by[0]) > 0:
            for i in range(len(fact_or_rule.supported_by)):
                spaces = ""
                for k in range(indents+2):
                    spaces += " "
                self.result += spaces + "SUPPORTED BY" + '\n'
                for support in fact_or_rule.supported_by[i]:
                    self.result += "  "
                    if isinstance(support, Fact):
                        next_fr = self._get_fact(support)
                        space = ""
                        for i in range(indents+2):
                            space += " "
                        self.result += space + "fact: " + str(next_fr.statement)
                        if not next_fr.supported_by:
                            self.result += " ASSERTED"
                        self.result += "\n"
                    elif isinstance(support, Rule):
                        next_fr = self._get_rule(support)
                        space = ""
                        for i in range(indents+2):
                            space += " "
                        self.result += space + "rule: ("
                        for i in range(len(next_fr.lhs)):
                            if i == len(next_fr.lhs) - 1:
                                self.result += str(next_fr.lhs[i])
                                break
                            self.result += str(next_fr.lhs[i]) + ", "
                        self.result += ") -> " + str(next_fr.rhs)
                        if not next_fr.supported_by:
                            self.result += " ASSERTED"
                        self.result += "\n"
                    else:
                        return
                    indents += 2

                    self.helper(next_fr, indents+2)

                    indents -= 2
        return self.result

    def find_in_kb(self, fact_or_rule):
        if isinstance(fact_or_rule, Fact) and fact_or_rule in self.facts:
            ind = self.facts.index(fact_or_rule)
            return self.facts[ind]
        elif isinstance(fact_or_rule, Rule) and fact_or_rule in self.rules:
            ind = self.rules.index(fact_or_rule)
            return self.rules[ind]
        else:
            return False
    def is_asserted(self, fact_or_rule):
        if not next_fr.supported_by:
            return True
        else:
            return False

    def make_str(self, length):
        s = ""
        for i in range(length):
            s += " "
        return s

class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules
        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase
        Returns:
            Nothing
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        # Student code goes here

        #

        binding = match(fact.statement, rule.lhs[0])

        if binding and len(rule.lhs) == 1:
            s = instantiate(rule.rhs, binding)
            # when do i construct fact with [fact,rule] vs [fact]???????????

            #only call constructor if new
            # find "f" in self.facts.. if not in self.facts construct new
            # otherwise append the supports_facts and supports_rules


            f = Fact(s, [fact,rule])
            #print(f.statement, '------------------------------------')

            kb.kb_assert(f)
            #print(',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,', type(f))

            fact.supports_facts.append(f)
            rule.supports_facts.append(f)
                #print('--------------\n\n', rule.supports_facts)
                #print([fact,rule], '\n\n=++++++++++++++++++++++++++++++++++++++++++++++++')


        elif binding and len(rule.lhs) > 1:
            s_r = instantiate(rule.rhs, binding)


            lhs_statements = []
            for i in rule.lhs:
                lhs_statements.append(instantiate(i, binding))

            del lhs_statements[0]

            # SAME LOGIC FOR RULE, BASED ON FACT
            new_rule = Rule([lhs_statements, s_r], [fact, rule])
            """
            if new_rule in kb.rules:
                ind = kb.rules.index(new_rule)
                kb.rules[ind].supported_by.append([fact,rule])
                rule.supports_rules.append(kb.rules[ind])
            else:
                """
            kb.kb_assert(new_rule)
            #print(new_rule.lhs, new_rule.rhs, '\n\n----------------------------')
            #print('--------------------------\n', new_rule.lhs, '\n', type(new_rule) , '-------------------')
            rule.supports_rules.append(new_rule)
            fact.supports_rules.append(new_rule)
                #print('-------------\n\n' , len(rule.supports_rules))
