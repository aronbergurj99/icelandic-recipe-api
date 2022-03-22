# icelandic-recipe-api
free REST API for recipes written in Icelandic. The API uses data from gottimatinn.is and is therefore only for non commercial purposes.
</br>
The API can be accessed at [api.uppskriftir.com](https://api.uppskriftir.com)

# Authentication
Before you can access any data from the API you will have to make an POST request to [/token](#post-token). This request will return a token that needs to be in headers under `Authorization`. 

# Endpoints

## POST
[/signup](#post-signup)</br>
[/token](#post-token)</br>
___
## GET
`Requires auth` [/recipes](#get-recipes)</br>
`Requires auth` [/recipes/{id}](#get-recipesid)</br>
`Requires auth` [/groups](#get-groups)</br>
`Requires auth` [/tags](#get-tags)</br>
___

### POST /signup

**Body**
```
{
    "username": "random@randomemail.com",
    "password": "strongpassword!1234"
}
```

**Response**
```
//On sucess
{
    "Detail": "successfully created user"
}
or

//If username is taken
{
    "detail": "Username is already taken"
}
```
___

### POST /token

**Body**
```
{
    "username": "random@randomemail.com",
    "password": "strongpassword!1234"
}
```
**Response**
```
//On sucess
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoicmFuZG9tQHJhbmRvbTNlbWFpbC5jb20iLCJyb2xlIjoidXNlciIsImV4cGlyZXMiOjE2NDcwOTQyMjEuNjY0OTA2fQ.PLvf70iLTpKdJgOKlvEyg95m9n2AOxcaXFNJFC28XR8",
    "token_type": "bearer"
}
or

//If incorrect username or password
{
    "detail": "Incorrect username or password"
}
```
___

### GET /recipes
**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `pageSize` | optional | int  | The number of recipes to get in one page. Defualt is `24` and max is `64`|
|     `page` | optional | int  | The page number. Default is `1`.    |
|     `groups` | optional | string | Filters recipies by group. Default is `None` | 
|     `tags` | optional | string | Filters recipes by tags. Default is `None` |
|     `random` | optional | bool| If set to true will return random recipes. Can be used with other params. <br/>Default is `false`|

**Response**
```
// Example response
[
    {
        "_id": "622bbbe46285ee795a73bd20",
        "name": "Fylltar döðlur í hnetuhjúp",
        "description": "Hér eru á ferðinni undurljúffengar döðlur í sparifötunum. Það er tilvalið að bjóða upp á þær sem forrétt, á smáréttarhlaðborði nú eða bara þegar ykkur langar í eitthvað gómsætt. Það tekur stutta stund að útbúa þennan rétt og hægt er að plasta þær og geyma í kæli yfir nótt sé þess óskað.",
        "url": "https://www.gottimatinn.is/uppskriftir/fylltar-dodlur-i-hnetuhjup",
        "image_url": "https://www.gottimatinn.is//media/1/fylltar-dodlur---gott-i-matinn-1.jpg",
        "ingredients": [
            {
                "step_name": "",
                "items": [
                    {
                        "qty": "15.0 stk.",
                        "ingredient": "ferskar döðlur"
                    },
                    {
                        "qty": "150.0 g",
                        "ingredient": "íslenskur mascarpone frá Gott í matinn"
                    },
                    {
                        "qty": "2.0 msk.",
                        "ingredient": "hunang"
                    },
                    {
                        "qty": "None None",
                        "ingredient": "saxaðar möndlur og hnetur að eigin vali, t.d. pekan-, kasjú-, pistasíu-, eða jarðhnetur"
                    }
                ]
            }
        ],
        "instructions": [
            {
                "title": "Aðferð",
                "steps": [
                    "Skerið rauf í döðlurnar, fjarlægið steininn og opnið „vasa“ í þær.",
                    "Blandið Mascarpone osti og hunangi saman í skál, setjið í sprautupoka/zip lock poka og fyllið „vasana“ á döðlunum.",
                    "Leggið rjómaostahliðina ofan í skál með söxuðum hnetum/möndlum og veltið aðeins um svo það festist vel af blöndu við hverja döðlu.",
                    "Geymið í kæli þar til bera á fram."
                ]
            }
        ],
        "tags": [
            "Einfalt",
            "Sætt og gott",
            "Smáréttir",
            "Konfekt",
            "Afmæli",
            "Fermingar",
            "Páskar",
            "Saumaklúbbar"
        ],
        "author": "Höfundur: Berglind Hreiðarsdóttir",
        "website": "https://www.gottimatinn.is/",
        "groups": [
            "Kvöldmatur"
        ]
    }
]
```
___

### GET /recipes/{id}

**Response**
```
//On success

    "_id": "622bbbe46285ee795a73bd20",
    "name": "Fylltar döðlur í hnetuhjúp",
    "description": "Hér eru á ferðinni undurljúffengar döðlur í sparifötunum. Það er tilvalið að bjóða upp á þær sem forrétt, á smáréttarhlaðborði nú eða bara þegar ykkur langar í eitthvað gómsætt. Það tekur stutta stund að útbúa þennan rétt og hægt er að plasta þær og geyma í kæli yfir nótt sé þess óskað.",
    "url": "https://www.gottimatinn.is/uppskriftir/fylltar-dodlur-i-hnetuhjup",
    "image_url": "https://www.gottimatinn.is//media/1/fylltar-dodlur---gott-i-matinn-1.jpg",
    "ingredients": [
        {
            "step_name": "",
            "items": [
                {
                    "qty": "15.0 stk.",
                    "ingredient": "ferskar döðlur"
                },
                {
                    "qty": "150.0 g",
                    "ingredient": "íslenskur mascarpone frá Gott í matinn"
                },
                {
                    "qty": "2.0 msk.",
                    "ingredient": "hunang"
                },
                {
                    "qty": "None None",
                    "ingredient": "saxaðar möndlur og hnetur að eigin vali, t.d. pekan-, kasjú-, pistasíu-, eða jarðhnetur"
                }
            ]
        }
    ],
    "instructions": [
        {
            "title": "Aðferð",
            "steps": [
                "Skerið rauf í döðlurnar, fjarlægið steininn og opnið „vasa“ í þær.",
                "Blandið Mascarpone osti og hunangi saman í skál, setjið í sprautupoka/zip lock poka og fyllið „vasana“ á döðlunum.",
                "Leggið rjómaostahliðina ofan í skál með söxuðum hnetum/möndlum og veltið aðeins um svo það festist vel af blöndu við hverja döðlu.",
                "Geymið í kæli þar til bera á fram."
            ]
        }
    ],
    "tags": [
        "Einfalt",
        "Sætt og gott",
        "Smáréttir",
        "Konfekt",
        "Afmæli",
        "Fermingar",
        "Páskar",
        "Saumaklúbbar"
    ],
    "author": "Höfundur: Berglind Hreiðarsdóttir",
    "website": "https://www.gottimatinn.is/",
    "groups": [
        "Kvöldmatur"
    ]
}

or

//On error
{
    "detail": "No recipe exists with supplied ID"
}
```
___

### GET /groups

**Response**
```
[
    "Kvöldmatur",
    "Bakstur",
    "Yfir daginn",
    "Hollusta"
]
```
___

### GET /tags

**Response**
```
[
    "Afmæli",
    "Aðrir kjötréttir",
    "Bakaðir ostar",
    "Bakstur",
    "Bollakökur og möffins",
    "Bolludagur",
    "Boozt drykkir",
    "Brauð",
    "Brauðréttir",
    "Brúðkaup",
    "Bóndadagur",
    "Dögurður (Brunch)",
    "Eftirréttir",
    "Einfalt",
    "Fermingar",
    "Fiskréttir",
    "Flókið",
    "Frakkland",
    "Gott í kvöldmatinn",
    "Grikkland",
    "Grænmetisréttir",
    "Hamborgarar",
    "Heilsuuppskriftir",
    "Hrekkjavaka",
    "Indland",
    "Jól",
    "Kaffidrykkir",
    "Kjúklingaréttir",
    "Konfekt",
    "Konudagur",
    "Kökur",
    "Lambakjöt",
    "Lágkolvetna réttir",
    "Léttir réttir",
    "Mexíkó",
    "Meðlæti",
    "Miðlungs",
    "Morgunmatur",
    "Nautakjöt",
    "Nesti",
    "Ostabakkar",
    "Ostakökur",
    "Ostar og ídýfur",
    "Ostaréttir",
    "Partý",
    "Pasta og bökur",
    "Pizzur",
    "Páskar",
    "Salöt",
    "Samlokur",
    "Saumaklúbbar",
    "Skyrkökur",
    "Smákökur",
    "Smáréttir",
    "Snúðar og horn",
    "Spánn",
    "Sumar",
    "Sætar sósur",
    "Sætt og gott",
    "Sósur",
    "Súpur",
    "Tilefni",
    "Um víða veröld",
    "Yfir daginn",
    "Ídýfur",
    "Ís",
    "Ítalía"
]
```
___


