package domain

import "errors"

var ErrUserNotFound = errors.New("failed to get user, user not found")

var ErrInvalidPassword = errors.New("failed to login, invalid password")

var ErrUserAlreadyExists = errors.New("failed to register, user already exists")

var ErrFailedRegister = errors.New("failed to register")
