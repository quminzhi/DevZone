# DevZone

Author: Minzhi Qu  Email: minzhq2@uw.edu

DevZone is a platform built for web app/service developers. Developers are free to share works in DevZone and build a solid connection with each other.

This is an oper-source project.

## Installation

### Prerequisite

- Django 4.0.*
- Python 3.8 (or newer)
- Django REST framework

### Docker

We also provide a container version for the project.

## Architecture

### Models

There are many models designed for the project, such as `review`, `vote`, `tag`, `message`. However, `user` (`profile`) and `project` are two models shaping the skeleton of the project.

- User Model: includes info for each user and personal access control.

```python
class User(AbstractUser):
    username = models.CharField(max_length=200, null=True, unique=True)
    name = models.CharField(max_length=200, null=True) # firstname
    email = models.EmailField(null=True, unique=True)
    bio = models.TextField(null=True, blank=True)

class Profile(models.Model):
    # mapping model to model
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to='profiles/', default='user-default.png')
    github = models.CharField(max_length=200, null=True, blank=True)
    website = models.CharField(max_length=200, null=True, blank=True)
    linkin = models.CharField(max_length=200, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
```

- Project Model: includes the exhibition of project and permission control for editing a project.

```python
class Project(models.Model):
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=CASCADE)
    title = models.CharField(max_length=200)
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    # null for database, blank for django to solve post request
    description = models.TextField(null=True, blank=True)
    # default and upload_to are based on MEDIA_ROOT
    featured_image = models.ImageField(
        null=True, blank=True, upload_to='projects/', default="default.jpg")  # search in static dir

    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    pos_ratio = models.IntegerField(default=0, null=True, blank=True)

    # TODO: many to many relationship
    tags = models.ManyToManyField('Tag', blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
```

`Project` to `Review` is a one-to-many mapping and `Project` to `Tag` is a many-to-many mapping.

### REST API

In addition to graphic controller, we provide RESTful API for CRUD operations.

```python
urlpatterns = [
    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('', views.getRoutes),
    
    path('projects/', views.getProjects),
    path('project/<str:pk>/', views.getProject),
    path('project/<str:pk>/vote/', views.projectVote),
    
    path('remove-tag/', views.removeTag),
    path('add-tag/', views.addTag),
]
```

## API Usage

We provide CRUD operations with REST APIs. In this section, we will illustrate how to use them with examples. Postman is suggestted to use to test APIs. The host ip is `18.222.17.102`.

### GET

- Get APIs

```bash
# request
GET {{HOST}}/api/projects/
```

```bash
# response
200OK 4 ms 664 B
[
    {
        "GET": "/api/projects/"
    },
    {
        "GET": "/api/project/id/"
    },
    {
        "POST": "/api/user/token/"
    },
    {
        "POST": "/api/user/token/refresh/"
    },
    {
        "POST": "/api/project/id/vote/"
    },
    {
        "DELETE": "/api/remove-tag/ (token required with 'api/user/token', tag id and project id in JSON)"
    },
    {
        "PUT": "/api/add-tag/ (token required with 'api/user/token', tag value and project id in JSON)"
    }
]
```

- Get projects

```bash
# request: "GET": "/api/projects/"
GET {{HOST}}/api/projects/
```

```bash
# response
[
    {
        "id": "abf00f48-b75d-4a62-8556-7328b191e140",
        "owner": {
            "id": "2051e91a-c852-4e9e-aea4-7f6974f1656d",
            "name": "minzhi",
            "email": "quminzhi@gmail.com",
            "username": "quminzhi",
            "location": "Tacoma, WA",
            "short_intro": "UW student",
            "bio": "Hello, I'm now a UW graduate student and cloud computing developer.",
            "profile_image": "/images/profiles/me_HlXxRMt.png",
            "github": "https://github.com/quminzhi",
            "website": null,
            "linkin": null,
            "created": "2022-02-17T21:57:56.814691Z",
            "user": 1
        },
        "tags": [
            {
                "id": "66a08b5b-4cf8-46a8-aad9-82612a64748c",
                "name": "Django"
            },
            {
                "id": "d11e4680-7a6b-4288-9a2b-128a00e68f6d",
                "name": "Python"
            }
        ],
        "reviews": [],
        "title": "HashDoc",
        "short_intro": "an online doc",
        "description": "This is an online doc. The doc server is built with Django and Bootstrap.",
        "featured_image": "/images/projects/design-h-05.jpg",
        "demo_link": null,
        "source_link": "https://github.com/quminzhi/HashDoc",
        "vote_total": 0,
        "pos_ratio": 0,
        "created": "2022-02-17T22:26:05.253979Z"
    },
    {
        "id": "db3c3347-f865-4ad1-805e-804c1974608a",
        "owner": {
            "id": "38600149-1df7-4edb-8d5f-b26aba396d1b",
            "name": "marty",
            "email": "minzhq2@uw.edu",
            "username": "marty",
            "location": "Seattle, WA",
            "short_intro": "UW student",
            "bio": "Hi, I'm marty, an undergraduate UW student.",
            "profile_image": "/images/profiles/lockdown.jpeg",
            "github": "https://github.com/quminzhi",
            "website": null,
            "linkin": null,
            "created": "2022-02-17T22:09:45.283146Z",
            "user": 2
        },
        "tags": [
            {
                "id": "5b4e80b8-c882-4a5c-9573-d96c9a47fab2",
                "name": "C"
            },
            {
                "id": "0a7fb25f-38cc-4c24-8b2d-64f5befa4415",
                "name": "SHELL"
            }
        ],
        "reviews": [],
        "title": "MASH",
        "short_intro": "a multi-process command-line tool",
        "description": "MASH is a multi-process command-line tool developed in C.",
        "featured_image": "/images/projects/design-h-08.jpg",
        "demo_link": "https://github.com/quminzhi/MASH",
        "source_link": "https://github.com/quminzhi/MASH",
        "vote_total": 0,
        "pos_ratio": 0,
        "created": "2022-02-17T22:17:47.971863Z"
    }
]
```

- Get specific project

```bash
# request: "GET": "/api/project/id/"
GET {{HOST}}/api/project/abf00f48-b75d-4a62-8556-7328b191e140/
```

```bash
# response:
{
    "id": "abf00f48-b75d-4a62-8556-7328b191e140",
    "owner": {
        "id": "2051e91a-c852-4e9e-aea4-7f6974f1656d",
        "name": "minzhi",
        "email": "quminzhi@gmail.com",
        "username": "quminzhi",
        "location": "Tacoma, WA",
        "short_intro": "UW student",
        "bio": "Hello, I'm now a UW graduate student and cloud computing developer.",
        "profile_image": "/images/profiles/me_HlXxRMt.png",
        "github": "https://github.com/quminzhi",
        "website": null,
        "linkin": null,
        "created": "2022-02-17T21:57:56.814691Z",
        "user": 1
    },
    "tags": [
        {
            "id": "66a08b5b-4cf8-46a8-aad9-82612a64748c",
            "name": "Django"
        },
        {
            "id": "d11e4680-7a6b-4288-9a2b-128a00e68f6d",
            "name": "Python"
        }
    ],
    "reviews": [],
    "title": "HashDoc",
    "short_intro": "an online doc",
    "description": "This is an online doc. The doc server is built with Django and Bootstrap.",
    "featured_image": "/images/projects/design-h-05.jpg",
    "demo_link": null,
    "source_link": "https://github.com/quminzhi/HashDoc",
    "vote_total": 0,
    "pos_ratio": 0,
    "created": "2022-02-17T22:26:05.253979Z"
}
```

### POST

Because the system is token-based, you are able to register your own account or use test account for obtaining an token for testing. `email: test@uw.edu` and `passwd: quminzhi123456`.

- Access token

The time to live for a token is 30 minutes.

```bash
# request: /api/user/token
POST {{HOST}}/api/user/token
with JSON body:
{
    "email": "test@uw.edu",
    "password": "quminzhi123456"
}
```

```bash
# response:
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0NTIyNDQ5MywiaWF0IjoxNjQ1MTM4MDkzLCJqdGkiOiI1NjM1ZDBjNDFkMTQ0OTQ1YWJmYmVjZmY4NWRjN2Q0YSIsInVzZXJfaWQiOjJ9.wY-WhnfcmHT4ghSSIky9vUPLtDQMRw5Ou_B5DURkLU0",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ1MTM5ODkzLCJpYXQiOjE2NDUxMzgwOTMsImp0aSI6IjJhZWUxNDBjZDg1ZTRhM2Y5YmZjMGIyYTRiMDkxYmMzIiwidXNlcl9pZCI6Mn0.ldVlgCf5GxeKSqSoDmDpkElup_a0W_Yy8vRJqz6aIQo"
}
```

- Vote for a project

This is an **update operation**. Since vote operation is login-required. So token needs to be sent with post request.

```bash
# request: /api/project/id/vote/
POST {{HOST}}/api/project/db3c3347-f865-4ad1-805e-804c1974608a/vote/
with Header Authorization: 
{ # your token
    Horizon eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ1MTM5ODkzLCJpYXQiOjE2NDUxMzgwOTMsImp0aSI6IjJhZWUxNDBjZDg1ZTRhM2Y5YmZjMGIyYTRiMDkxYmMzIiwidXNlcl9pZCI6Mn0.ldVlgCf5GxeKSqSoDmDpkElup_a0W_Yy8vRJqz6aIQo
}
with JSON body: 
{
    "value": "up" # or "down"
}
```

```bash
# response:
{
    "Vote success"
}

# check if the vote of the project changes with GET /api/project/id/
{
    "id": "db3c3347-f865-4ad1-805e-804c1974608a",
    "owner": {
        "id": "38600149-1df7-4edb-8d5f-b26aba396d1b",
        "name": "marty",
        "email": "minzhq2@uw.edu",
        "username": "marty",
        "location": "Seattle, WA",
        "short_intro": "UW student",
        "bio": "Hi, I'm marty, an undergraduate UW student.",
        "profile_image": "/images/profiles/lockdown.jpeg",
        "github": "https://github.com/quminzhi",
        "website": null,
        "linkin": null,
        "created": "2022-02-17T22:09:45.283146Z",
        "user": 2
    },
    "tags": [
        {
            "id": "5b4e80b8-c882-4a5c-9573-d96c9a47fab2",
            "name": "C"
        },
        {
            "id": "0a7fb25f-38cc-4c24-8b2d-64f5befa4415",
            "name": "SHELL"
        }
    ],
    "reviews": [
        {
            "id": "55515292-272a-4372-85e7-30bc96d19a9d",
            "body": null,
            "value": "up",
            "created": "2022-02-17T23:13:11.837341Z",
            "owner": "38600149-1df7-4edb-8d5f-b26aba396d1b",
            "project": "db3c3347-f865-4ad1-805e-804c1974608a"
        }
    ],
    "title": "MASH",
    "short_intro": "a multi-process command-line tool",
    "description": "MASH is a multi-process command-line tool developed in C.",
    "featured_image": "/images/projects/design-h-08.jpg",
    "demo_link": "https://github.com/quminzhi/MASH",
    "source_link": "https://github.com/quminzhi/MASH",
    "vote_total": 1,    # <=== vote success
    "pos_ratio": 100,
    "created": "2022-02-17T22:17:47.971863Z"
}
```

### DELETE and PUT

Each project has many tags related to it. For example, `MASH` project has `C` and `Kubernetes` tags. Now let's try to create and delete tags for a project.

- Delete tag (Token needed)

We must provide `project id` and `tag id`, which you can access from `GET` operation before.

**NOTE: you are ONLY able to remove tags on your project.**

```bash
# request: /api/remove-tag/
DELETE {{HOST}}/api/remove-tag/
with Token in Header
{ # your token
    Horizon eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ1MTM5ODkzLCJpYXQiOjE2NDUxMzgwOTMsImp0aSI6IjJhZWUxNDBjZDg1ZTRhM2Y5YmZjMGIyYTRiMDkxYmMzIiwidXNlcl9pZCI6Mn0.ldVlgCf5GxeKSqSoDmDpkElup_a0W_Yy8vRJqz6aIQo
}
with JSON body
{
    "project": "db3c3347-f865-4ad1-805e-804c1974608a", # project id, this is must be YOUR project!!!
    "tag": "0a7fb25f-38cc-4c24-8b2d-64f5befa4415" # tag id associated with the project
}
```

```bash
# response:
Tag was deleted

# check the project with /api/project/id/
{
    "id": "db3c3347-f865-4ad1-805e-804c1974608a",
    ...
    "tags": [
        {
            "id": "66a08b5b-4cf8-46a8-aad9-82612a64748c",
            "name": "Django"
        },
        # deleted
        # {
        #     "id": "d11e4680-7a6b-4288-9a2b-128a00e68f6d",
        #     "name": "Python"
        # }
    ],
    ...
}
```

- Add tag (Token needed)

In this case, we need to provide `project id` and `tag value` (like `C++`).

**NOTE: you are ONLY able to add tags on your project.**

```bash
# request: /api/add-tag/
PUT {{HOST}}/api/remove-tag/
with Token in Header
{ # your token
    Horizon eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ1MTM5ODkzLCJpYXQiOjE2NDUxMzgwOTMsImp0aSI6IjJhZWUxNDBjZDg1ZTRhM2Y5YmZjMGIyYTRiMDkxYmMzIiwidXNlcl9pZCI6Mn0.ldVlgCf5GxeKSqSoDmDpkElup_a0W_Yy8vRJqz6aIQo
}
with JSON body
{
    "project": "db3c3347-f865-4ad1-805e-804c1974608a", # project id, this is must be YOUR project!!!
    "tag": "C++" # tag value
}
```

```bash
# response:
Tag was added

# check the project with /api/project/id/
{
    "id": "db3c3347-f865-4ad1-805e-804c1974608a",
    ...
    "tags": [
        {
            "id": "66a08b5b-4cf8-46a8-aad9-82612a64748c",
            "name": "Django"
        },
        # C++ added
        {
            "id": "d993kds80-5a6b-1987-952b-12ds00e68f6d",
            "name": "C++"
        }
    ],
    ...
}
```