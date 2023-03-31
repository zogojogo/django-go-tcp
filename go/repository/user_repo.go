package repository

import (
	"gorm.io/gorm"
)

type UserRepo interface {
}

type userRepoImpl struct {
	db *gorm.DB
}

func NewUserRepo(db *gorm.DB) UserRepo {
	return &userRepoImpl{db}
}
