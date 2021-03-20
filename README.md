# Cosmic Chem

README in progress

Samuel Gunter

Purpose: To automatically balance chemical equations, with options explanations, to quiz on balancing equations, and to validate possible solutions

How it works: When input it received, it first validates the chemical equation with a Regular Expression, then it parses the equation into a matrix where each column in a compound, each row is an element, and the intersection is how many moles of the specific element in that compound. It then transforms the matrix into the "Row Reduced Echelon Form", grabs the last column, finds the greatest common denominator, multiples that column by the gcd, and that is your coefficients for the compounds, except the last compound's coefficient is just the gcd from before.
