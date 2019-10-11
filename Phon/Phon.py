# coding: UTF-8
__author__ = 'Steeve'
__version__ = '1.0.0'

import os
import re
import argparse

class GenericAplication():
    def __init__(self, arquivo):
        self.arquivo = arquivo

    def __splitGetData(self, text, by, index):
        if not type(text) == str and hasattr(text, 'text'):
            text = text.text
        if type(text) == str:
            if type(by) == list:
                for b in by[1:]:
                    text = text.replace(b, by[0])
                by = by[0]
            if index < 0:
                index = len(text.split(by))-1
            return text.split(by)[index]
        elif type(text) == list:
            lst = []
            for x in text:
                lst.append(self.__splitGetData(x, by, index))
            return lst
        return text

    def __getRotulo(self, name, objRot):
        for rot in objRot:
            if name == rot['rotulo']:
                return rot                           
        return 'No Existe este rotulo'

    def __conjInstrucoes(self, name):        
        conjinstru = [{
            'opcode' : '00',
            'name': 'NOP',
            'tamanho': 1
        },{
            'opcode' : '10',
            'name': 'LDR',
            'tamanho': 2
        },{
            'opcode' : '20',
            'name': 'STR',
            'tamanho': 2
        },{
            'opcode' : '30',
            'name': 'ADD',
            'tamanho': 2
        },{
            'opcode' : '40',
            'name': 'SUB',
            'tamanho': 2
        },{
            'opcode' : '50',
            'name': 'MUL',
            'tamanho': 2
        },{
            'opcode' : '60',
            'name': 'DIV',
            'tamanho': 2
        },{
            'opcode' : '70',
            'name': 'NOT',
            'tamanho': 1
        },{
            'opcode' : '80',
            'name': 'AND',
            'tamanho': 2
        },{
            'opcode' : '90',
            'name': 'OR',
            'tamanho': 2
        },{
            'opcode' : 'A0',
            'name': 'XOR',
            'tamanho': 2
        },{
            'opcode' : 'B0',
            'name': 'JMP',
            'tamanho': 2
        },{
            'opcode' : 'C0',
            'name': 'JEQ',
            'tamanho': 2
        },{
            'opcode' : 'D0',
            'name': 'JG',
            'tamanho': 2
        },{
            'opcode' : 'E0',
            'name': 'JL',
            'tamanho': 2
        },{
            'opcode' : 'F0',
            'name': 'HLT',
            'tamanho': 1
        },{            
            'name': 'byte',
            'tamanho': 1
        }]

        for inst in conjinstru:            
            if name == inst['name']:                                
                return inst
        return None


    def programaBinaria(self):        
        simbolData = []
        programBinary = []        
        endAtual = 0

        fileData = open(self.arquivo, 'r')
        lines  = fileData.readlines()
        
        for x in range(2):
            if x==0: # Primeira pasagem pegando os rotulos e o endereço da memoria                
                for l in lines:                                                            
                    for g in l.split():                        
                        result = re.search(':', g)                                            
                        if result != None:
                            # print(endAtual,' Rotulos '+' - '+self.__splitGetData(g,':',0))
                            simbolData.append({
                                "rotulo" : self.__splitGetData(l,':',0),
                                "end" : endAtual
                            })
                        
                        if self.__conjInstrucoes(g.strip()) != None:
                            # print(endAtual,' - ',g)
                            if g != 'text':                            
                                endAtual += self.__conjInstrucoes(g.strip())['tamanho']

                        if g == 'data':                                    
                            endAtual = 128                                                                                            
                # print(simbolData)
                                        
            else: # Segunda pasagem pasagem pegando os rotulos e o endereço da memoria                               
                endAtual = 0
                for l in lines:                                                            
                    for g in l.split():                        
                        result = re.search(':', g)                                            
                        if result == None:                                                    
                            if g != 'text' and g != 'byte' and g != 'data':                                                                               
                                if self.__conjInstrucoes(g.strip()) != None:
                                    # print(endAtual,' Intrucoes ',self.__conjInstrucoes(g.strip()))                                    
                                    programBinary.append({
                                        'end' : endAtual,
                                        'conteudo' : bin(int(self.__conjInstrucoes(g.strip())['opcode'], 16))[2:].zfill(8)                                  
                                    })
                                elif endAtual < 128 and self.__conjInstrucoes(g.strip()) == None:
                                    endRot = self.__getRotulo(g.strip(),simbolData)['end']
                                    # print(endAtual,' Operando ',endRot)
                                    programBinary.append({
                                        'end' : endAtual,
                                        'conteudo' : bin(int(str(endRot), 16))[2:].zfill(8)                                  
                                    })                                                                                                        
                                else:
                                    # print(endAtual,' Intrucoes ',g)
                                    programBinary.append({
                                        'end' : endAtual,
                                        'conteudo' : bin(int(g, 16))[2:].zfill(8)                                  
                                    })                                                                    
                                    
                                                                
                            if g != 'text' and g != 'byte':  
                                endAtual += 1
                                if g == 'data':                                    
                                    endAtual = 128



                arquivo = open("data.bin", "wb")                
                for pb in programBinary:
                    # print(pb['end'],'  ',pb['conteudo'])
                    arquivo.write(str(pb['end']))
                    arquivo.write(' ')
                    arquivo.write(pb['conteudo'])
                    arquivo.write('\n')
                arquivo.close()                



if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--arq', required=True, help='ASAMBLY file with data')

    args = parser.parse_args()
    GenericAplication(arquivo=args.arq).programaBinaria()

    # Example
    # python Phon.py --arq data.txt
# print(len(l.split()),' - ',l.split())                                        