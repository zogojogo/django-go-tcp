package usecase

import (
	"entry_task/domain"
	"entry_task/dto"
	"entry_task/entity"
	"entry_task/repository"
	"entry_task/util"
)

type AuthUsecase interface {
	Login(data dto.LoginRequestDTO) (*dto.AuthResponseDTO, error)
	Register(data dto.RegisterRequestDTO) (*dto.AuthResponseDTO, error)
}

type authUsecaseImpl struct {
	userRepo repository.UserRepo
	authUtil util.AuthUtil
}

type AuthUsecaseConfig struct {
	UserRepo repository.UserRepo
	AuthUtil util.AuthUtil
}

func NewAuthUsecase(config *AuthUsecaseConfig) AuthUsecase {
	return &authUsecaseImpl{userRepo: config.UserRepo, authUtil: config.AuthUtil}
}

func (u authUsecaseImpl) Login(data dto.LoginRequestDTO) (*dto.AuthResponseDTO, error) {
	user, err := u.userRepo.GetByUsername(data.Username)
	if err != nil {
		return nil, err
	}
	if !u.authUtil.ComparePassword(user.Password, data.Password) {
		return nil, domain.ErrInvalidPassword
	}
	token, err := u.authUtil.GenerateAccessToken(user)
	if err != nil {
		return nil, err
	}
	return &dto.AuthResponseDTO{Token: token}, nil
}

func (u authUsecaseImpl) Register(data dto.RegisterRequestDTO) (*dto.AuthResponseDTO, error) {
	user := &entity.User{
		Username: data.Username,
		Email:    data.Email,
	}
	hashedPwd, err := u.authUtil.HashAndSalt(data.Password)
	if err != nil {
		return nil, err
	}
	user.Password = hashedPwd
	err = u.userRepo.Create(user)
	if err != nil {
		return nil, err
	}
	token, err := u.authUtil.GenerateAccessToken(user)
	if err != nil {
		return nil, err
	}
	return &dto.AuthResponseDTO{Token: token}, nil
}
