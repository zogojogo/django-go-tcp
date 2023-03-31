package util

import (
	"entry_task/config"
	"entry_task/dto"
	"entry_task/entity"
	"strconv"
	"time"

	"github.com/golang-jwt/jwt/v4"
	"golang.org/x/crypto/bcrypt"
)

type AuthUtil interface {
	GenerateAccessToken(user *entity.User) (string, error)
	ComparePassword(hashedPwd string, inputPwd string) bool
	HashAndSalt(pwd string) (string, error)
}

type authUtilImpl struct {
	envConfig *config.Config
}

func NewAuthUtil() AuthUtil {
	return &authUtilImpl{envConfig: config.NewConfig()}
}

type CustomClaim struct {
	jwt.RegisteredClaims
	User *dto.JwtResponse `json:"user"`
}

func (a *authUtilImpl) GenerateAccessToken(user *entity.User) (string, error) {
	envs := a.envConfig.AuthConfig
	dtoResponse := &dto.JwtResponse{
		UserId:   user.ID,
		Username: user.Username,
	}
	exp, _ := strconv.Atoi(envs.ExpiresIn)
	dur := time.Duration(exp) * time.Minute
	claims := &CustomClaim{
		jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(dur)),
			Issuer:    "entry-task-be-mpo",
			IssuedAt:  jwt.NewNumericDate(time.Now()),
		},
		dtoResponse,
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	hmacSampleSecret := envs.SecretKey
	tokenString, err := token.SignedString([]byte(hmacSampleSecret))

	if err != nil {
		return "", err
	}
	return tokenString, nil
}

func (a *authUtilImpl) ComparePassword(hashedPwd string, inputPwd string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(hashedPwd), []byte(inputPwd))
	return err == nil
}

func (u *authUtilImpl) HashAndSalt(pwd string) (string, error) {
	hash, err := bcrypt.GenerateFromPassword([]byte(pwd), bcrypt.MinCost)
	if err != nil {
		return "", err
	}
	return string(hash), nil
}
