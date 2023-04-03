package domain

import "errors"

var ErrUserNotFound = errors.New("failed to get user, user not found")

var ErrInvalidPassword = errors.New("the password is invalid")

var ErrUserAlreadyExists = errors.New("failed to register, user already exists")
