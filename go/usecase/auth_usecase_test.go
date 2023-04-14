package usecase_test

import (
	"entry_task/domain"
	"entry_task/dto"
	"entry_task/entity"
	mocks "entry_task/mocks/repository"
	mocks2 "entry_task/mocks/util"
	"entry_task/usecase"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestLogin(t *testing.T) {
	givenEmail := "zogojogo"
	expectedUser := entity.User{
		ID:       1,
		Email:    "zogojogo",
		Password: "$2a$04$hYffLZBb7eIillz/f2s7JuD6YBVGFra6fFsKcI6ES48RIWiEolxBm",
	}
	givenLoginRequest := dto.LoginRequestDTO{
		Username: "zogojogo",
		Password: "password1",
	}
	t.Run("should return invalid user if gorm can't find user", func(t *testing.T) {
		userRepoMock := mocks.NewUserRepo(t)
		authMocks := mocks2.NewAuthUtil(t)
		authUCConfig := usecase.AuthUsecaseConfig{
			UserRepo: userRepoMock,
			AuthUtil: authMocks,
		}
		authUC := usecase.NewAuthUsecase(&authUCConfig)

		userRepoMock.On("GetByUsername", givenEmail).Return(nil, domain.ErrUserNotFound)
		res, err := authUC.Login(dto.LoginRequestDTO{Username: "zogojogo"})

		assert.EqualError(t, err, domain.ErrUserNotFound.Error())
		assert.Nil(t, res)
	})

	t.Run("should return invalid password if input password isn't same with stored password", func(t *testing.T) {
		userRepoMock := mocks.NewUserRepo(t)
		authMocks := mocks2.NewAuthUtil(t)
		authUCConfig := usecase.AuthUsecaseConfig{
			UserRepo: userRepoMock,
			AuthUtil: authMocks,
		}
		authUC := usecase.NewAuthUsecase(&authUCConfig)

		userRepoMock.On("GetByUsername", expectedUser.Email).Return(&expectedUser, nil)
		authMocks.On("ComparePassword", expectedUser.Password, givenLoginRequest.Password).Return(false)
		res, err := authUC.Login(givenLoginRequest)

		assert.EqualError(t, err, domain.ErrInvalidCredentials.Error())
		assert.Nil(t, res)
	})

	t.Run("should return error internal server if failed to generate token", func(t *testing.T) {
		userRepoMock := mocks.NewUserRepo(t)
		authMocks := mocks2.NewAuthUtil(t)
		authUCConfig := usecase.AuthUsecaseConfig{
			UserRepo: userRepoMock,
			AuthUtil: authMocks,
		}
		authUC := usecase.NewAuthUsecase(&authUCConfig)

		userRepoMock.On("GetByUsername", expectedUser.Email).Return(&expectedUser, nil)
		authMocks.On("ComparePassword", expectedUser.Password, givenLoginRequest.Password).Return(true)
		authMocks.On("GenerateAccessToken", &expectedUser).Return("", domain.ErrInternalServerError)
		res, err := authUC.Login(givenLoginRequest)

		assert.EqualError(t, err, domain.ErrInternalServerError.Error())
		assert.Nil(t, res)
	})

	t.Run("should return token in dto.LoginResponse object type", func(t *testing.T) {
		userRepoMock := mocks.NewUserRepo(t)
		authMocks := mocks2.NewAuthUtil(t)
		authUCConfig := usecase.AuthUsecaseConfig{
			UserRepo: userRepoMock,
			AuthUtil: authMocks,
		}
		authUC := usecase.NewAuthUsecase(&authUCConfig)

		userRepoMock.On("GetByUsername", expectedUser.Email).Return(&expectedUser, nil)
		authMocks.On("ComparePassword", expectedUser.Password, givenLoginRequest.Password).Return(true)
		authMocks.On("GenerateAccessToken", &expectedUser).Return("testtoken", nil)
		res, err := authUC.Login(givenLoginRequest)

		assert.NoError(t, err)
		assert.NotNil(t, res)
	})
}

func TestRegister(t *testing.T) {
	givenDto := dto.RegisterRequestDTO{
		Email:    "test@gmail.com",
		Password: "testpassword",
		Username: "zogojogo",
	}
	givenUser := &entity.User{
		Email:    "test@gmail.com",
		Password: "zogoz",
		Username: "zogojogo",
	}
	t.Run("should error if failed to hash password", func(t *testing.T) {
		userRepoMocks := mocks.NewUserRepo(t)
		authUtilMocks := mocks2.NewAuthUtil(t)
		authUCConfig := usecase.AuthUsecaseConfig{
			UserRepo: userRepoMocks,
			AuthUtil: authUtilMocks,
		}

		authUtilMocks.On("HashAndSalt", "testpassword").Return("", domain.ErrInternalServerError)
		authUC := usecase.NewAuthUsecase(&authUCConfig)
		res, err := authUC.Register(givenDto)

		assert.EqualError(t, err, domain.ErrInternalServerError.Error())
		assert.Nil(t, res)
	})
	t.Run("should error if failed to register", func(t *testing.T) {
		userRepoMocks := mocks.NewUserRepo(t)
		authUtilMocks := mocks2.NewAuthUtil(t)
		authUCConfig := usecase.AuthUsecaseConfig{
			UserRepo: userRepoMocks,
			AuthUtil: authUtilMocks,
		}

		authUtilMocks.On("HashAndSalt", "testpassword").Return("zogoz", nil)
		userRepoMocks.On("Create", givenUser).Return(domain.ErrFailedRegister)
		authUC := usecase.NewAuthUsecase(&authUCConfig)
		res, err := authUC.Register(givenDto)

		assert.EqualError(t, err, domain.ErrFailedRegister.Error())
		assert.Nil(t, res)
	})

	t.Run("should error if failed to generate token", func(t *testing.T) {
		userRepoMocks := mocks.NewUserRepo(t)
		authUtilMocks := mocks2.NewAuthUtil(t)
		authUCConfig := usecase.AuthUsecaseConfig{
			UserRepo: userRepoMocks,
			AuthUtil: authUtilMocks,
		}

		authUtilMocks.On("HashAndSalt", "testpassword").Return("zogoz", nil)
		userRepoMocks.On("Create", givenUser).Return(nil, domain.ErrFailedRegister)
		authUtilMocks.On("GenerateAccessToken", givenUser).Return("", domain.ErrFailedRegister)
		authUC := usecase.NewAuthUsecase(&authUCConfig)
		res, err := authUC.Register(givenDto)

		assert.EqualError(t, err, domain.ErrFailedRegister.Error())
		assert.Nil(t, res)
	})

	t.Run("should error if success to register", func(t *testing.T) {
		userRepoMocks := mocks.NewUserRepo(t)
		authUtilMocks := mocks2.NewAuthUtil(t)
		authUCConfig := usecase.AuthUsecaseConfig{
			UserRepo: userRepoMocks,
			AuthUtil: authUtilMocks,
		}

		authUtilMocks.On("HashAndSalt", "testpassword").Return("zogoz", nil)
		userRepoMocks.On("Create", givenUser).Return(nil)
		authUtilMocks.On("GenerateAccessToken", givenUser).Return("testToken", nil)
		authUC := usecase.NewAuthUsecase(&authUCConfig)
		res, err := authUC.Register(givenDto)

		assert.NoError(t, err)
		assert.NotNil(t, res)
	})
}
