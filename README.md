
RESOURCE: Operators (from the game Rainbow Six Siege)
name, country, side, weapon, age.

*id PRIMARY KEY integer

*name TEXT

*country TEXT

*side TEXT

*weapon TEXT

*age integer

RESOURCE: Users (to authenticate to my website)

username, first_name, last_name, hash_password 

(Note: username are email, just I name it that way before I realize I needed it be name email)

*id PRIMARY KEY integer

*username TEXT

*first_name TEXT

*last_name TEXT

*hash_password TEXT


|id | name     | country     | side       | weapon       | age       |
|---|----------|-------------|------------|--------------|-----------|
|1  | Doc      | france      | defending  | rifle        | 33        |
|2  | Rook      | france     | defending  | pistol       | 40        |
|3  | Rando      | Iceland   | attacking  | revelor      | 32        |
|4  | Fuze      | Russian    | burden     | sniper       | 29        |

|id | username     | first_name     | last_name       | hash_password       |
|---|--------------|----------------|-----------------|---------------------|
|1  | mama@gmail.com| sandra        | feildmen        | $2b$12$OLIYl4AsuE6NfNq6ydwOeeIOOFDCdNJ9An7TjNJTKVoUNtfoqf1cK| 
|2  | ioi@gmail.com | agent         | killer          | YUA31Flo05GwinOKTRBOpOFnuWMSV2ZMcpx0hUeMenOVppbAnKNeO       |
|3  | test@gmail.com| guy           | dude            | 2b$12$s9R3/G1tk/OyMAgQjeJ3reypgIr3xhFZC3Et5jfrSGmp5PHkax0L2|
|4  | gamer@gmail.com| james         | bond            | $2b$12$9ke7Bq5ufGPknVI1CTjjBeiLR.OAKGojoOSeC40q8dXAF.Z9bH63O|

list (method: GET, Path: http://localhost:8080/operartors/ )

create (method: POST, Path: http://localhost:8080/operartors/)

retrive (method: GET, Path: http://localhost:8080/operartors/${opClientInfo.id}) 

modify (method: PUT, Path: http://localhost:8080/operartors/${opClientInfo.id})

delete (method: DELETE, Path: http://localhost:8080/operartors /${opClientInfo.id})

loginClient (method: POST, Path: http://localhost:8080/sessions )

logoutClient (method: DELETE, Path: http://localhost:8080/sessions )

registerClient (method: POST, Path: http://localhost:8080/users )







