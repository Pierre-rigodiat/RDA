# Automatic Key/Keyref instructions

The MDCS provides mechanisms for the automatic generation of XSD keys and associated keyrefs. This document describes how to create a key generator and how to add it into an XML schema. Generated keys are then made available in associated keyrefs via a drop down menu.

## Creating a key generator

The key generator will be used to create a new key every time an element containing a key is added to the form. The key generators are simply modules. Please refer to the module developer guide for more details about modules.

The signature of a key generator function should be the following:
```python
def function(values)
```
The *values* parameter will contain the list of existing values for this key generator.

The *examples* package contains some predefined key generators that can be used directly in the MDCS:
- **Random Integer**: generates a unique random integer for the key. The *values* parameter will be used to check the uniqueness of the key.
- **Random String**: generates a unique random string for the key. The *values* parameter will be used to check the uniqueness of the key.
- **Sequence of Integer**: generates a unique integer for the key. The *values* parameter will be used to select the next integer in the sequence.

Once written, the key generator function can be made available by adding a URL to the module package. By convention, the URL should start by *auto-key* to be recognized as an automatic key by the MDCS.

## Adding a key generator to an XML schema

Once created, the key generator can be associated to a key element in an XML schema. The process is the same as adding a module to a schema.
- Go to the template section of the admin dashboard and click on the *Modules* link of a template,
- Select a key element: a list of available key generators will appear,
- Select a key generator to associate with the key.

## Example

The following schema can be loaded in the MDCS to test the automatic key/keyref feature. A key generator is already associated to the schema.

```xml
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" elementFormDefault="qualified">
    <xs:element name="root">
        <xs:complexType>
            <xs:sequence>
                <xs:element name="component" maxOccurs="unbounded">                    
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="name" type="xs:string"/>
                        </xs:sequence>
                        <xs:attribute name="id" type="xs:string"/>
                    </xs:complexType>
                </xs:element>
                <xs:element name="items">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="item" maxOccurs="unbounded">
                                <xs:complexType>
                                    <xs:sequence>
                                        <xs:element name="component">
                                            <xs:complexType>
                                                <xs:attribute name="id" type="xs:string"/>
                                            </xs:complexType>
                                        </xs:element>
                                    </xs:sequence>
                                </xs:complexType>
                            </xs:element>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>
            </xs:sequence>
        </xs:complexType>
        <xs:key xmlns:ns0="http://mdcs.ns" name="componentKey" ns0:_mod_mdcs_="/examples/auto-key-seqint">
            <xs:selector xpath="component"/>
            <xs:field xpath="@id"/>            
        </xs:key>
        <xs:keyref name="componentKeyref" refer="componentKey">
            <xs:selector xpath="items/item/component"/>
            <xs:field xpath="@id"/>
        </xs:keyref>
    </xs:element>
</xs:schema>
```