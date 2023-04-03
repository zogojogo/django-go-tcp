package repository

import (
	"entry_task/domain"
	"entry_task/entity"
	"errors"

	"github.com/go-sql-driver/mysql"
	"gorm.io/gorm"
)

type UserRepo interface {
	GetByUsername(username string) (*entity.User, error)
	Create(user *entity.User) error
}

type userRepoImpl struct {
	db *gorm.DB
}

func NewUserRepo(db *gorm.DB) UserRepo {
	return &userRepoImpl{db}
}

const (
	DuplicateErrorConst uint16 = 1062
)

func (r userRepoImpl) GetByUsername(username string) (*entity.User, error) {
	var user *entity.User
	err := r.db.Where("username = ?", username).First(&user).Error
	if err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, domain.ErrUserNotFound
		}
		return nil, domain.ErrInternalServerError
	}
	return user, nil
}

func (r userRepoImpl) Create(user *entity.User) error {
	err := r.db.Create(user).Error
	if err != nil {
		if mySqlErr, ok := err.(*mysql.MySQLError); ok {
			if mySqlErr.Number == DuplicateErrorConst {
				return domain.ErrUserAlreadyExists
			}
		}
		return domain.ErrInternalServerError
	}
	return nil
}
