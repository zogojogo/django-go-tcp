package usecase

import (
	"entry_task/repository"
	"entry_task/util"
)

type AuthUsecase interface {
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
