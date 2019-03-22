# API

## Generates a card

Done in admin.

## GET /api/cards/<uuid>

### Output:
```
[{
    id: uuid,
    original_user: uuid,
    url: url,
    qr_code_url: url,             # path to image
    created_at: timestamp,
    modified_at: timestamp,
    current_user: {              # current User
        id: uuid,
        first_name: string,
        last_name: string,
        mobile: string,
        company: string,
        email: email,          # required
        address: {
            street: string
            postcode: string
            city: string
            country: string
        },
        birthday: date
        url: url
        social_profile: url
    },
    previousUser: {              # current User always has access to whomever gave him the card
        id: uuid,
        first_name: string,
        last_name: string,
        mobile: string,
        company: string,
        email: email,
        address: {
            street: string
            postcode: string
            city: string
            country: string
        },
        birthday: date
        url: url
        social_profile: url
    }
}]
```

## GET api/cards/card-id/history

Show all users who used the card starting at logged in user minus 1.

History tracking.

### Output:

```
{
    id: uuid,
    created_at: timestamp,
    modified_at: timestamp,
    users:
    [
        {
            id: uuid,
            first_name: string,
            last_name: string,
            mobile: string,
            email: email,
            company: string,
            address: {
                street: string
                postcode: string
                city: string
                country: string
            },
            birthday: date
            url: url
            social_profile: url
        }
    ]
}
```

## POST /api/cards/card-id/users

TTake over a card. Done in admin for now.

