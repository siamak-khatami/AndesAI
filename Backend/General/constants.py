class TableNames:
    UserTourVisibility = "user_tour_visibility"
    UserTours = "user_tours"
    Authors = "authors"
    Books = "books"
    Publishers = "publishers"
    Users = "users"


class FieldNames:
    TourName = "tour_name"
    TourID = "tour_id"
    IsEnabled = "is_enabled"
    RegTime = "registration_time"
    Password = "password"
    Mobile = "mobile"
    CountryIso = "country_iso"
    Family = "family"
    Email = "email"
    UserID = "user_id"
    UserPubID = "user_public_id"
    ID = "id"
    Name = "name"
    CreatedAt = "created_at"
    UpdatedAt = "updated_at"
    DeletedAt = "deleted_at"
    Title = "title"
    ISBN = "isbn"
    Year = "year"
    AuthorID = "author_id"
    PublisherID = "publisher_id"


class Consts:
    UserEmailActivation = 30
    ResetPassTokenTime = 30
    example = "example"
    UserActivationTime = 1440


class OnDelete:
    CASCADE = "CASCADE"
    NULL = "SET NULL"
    RESTRICT = "RESTRICT"
    NO_ACTION = "NO ACTION"
    DEFAULT = "SET DEFAULT"


class EndPoints:
    ChatLLM = "/chat_llm"
    LLMModels = "/llm_models"
    UserTours = "/user_tours"
    DeleteUser = "/delete-user"
    UpdateUser = "/update-user"
    ResetPass = "/reset-password"
    UpdatePass = "/update-password"
    UpdatePassToken = "/update-password-token"
    CheckLogin = "/check-login"
    LocalHostFrontEnd = "http://localhost:3000"
    ProductionHostFrontEnd = "https://example.com"
    ResendUserActivation = "/resend_user_activation"
    UserActivationRoot = "/activate_user"
    RegisterUser = "/register"
    Login = "/login"
    Users = "/users"
    LLMs = "/llms"
    Books = "/books"


class LLMS:
    LLMModels = ["NousResearch/Llama-2-7b-chat-hf",
                 "microsoft/Phi-3-mini-4k-instruct"]
    EmbeddingModel = "sentence-transformers/all-mpnet-base-v2"
